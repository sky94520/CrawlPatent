# -*- coding: utf-8 -*-
import scrapy
import os
import re
import json
import time
from urllib.parse import quote
import random
import redis
from urllib.parse import urlencode

from scrapy import Request
from CrawlPatent.items import PatentItem


class DetailSpider(scrapy.Spider):
    name = 'detail'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # 使用哪个
        REDIS_DB = int(os.getenv('REDIS_DB', 5))
        REDIS_CONFIG = crawler.settings.get('REDIS_CONFIG')
        REDIS_CONFIG['db'] = REDIS_DB

        spider = cls(REDIS_CONFIG, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def __init__(self, redis_config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = redis.StrictRedis(**redis_config, decode_responses=True)
        self.pattern = re.compile(r'.*?【(.*?)】.*?')
        # 计数器 用于统计在各个json文件中已经抓取到的链接
        self.counter = {}
        # 连续出错计数器
        self.err_count = 0
        self.base_url = 'http://dbpub.cnki.net/grid2008/dbpub/detail.aspx'

    def start_requests(self):
        for datum in self.get_links():
            yield self.create_request(datum)

    def get_links(self):
        """
        遍历文件夹，找出还未访问过的页面，之后yield
        :return:
        """
        # 获取链接的位置
        basedir = self.settings.get('BASEDIR')
        path = os.path.join(basedir, 'files', 'page_links')
        # 遍历整个page_links文件夹
        for parent, dirnames, filenames in os.walk(path, followlinks=True):
            category_code = os.path.split(parent)[-1]
            # 遍历所有的文件
            for filename in filenames:
                full_filename = os.path.join(parent, filename)
                # 来源文件判断该文件是否已经访问过了
                source = '%s/%s' % (category_code, filename)
                if self.db.sismember('page_links', source):
                    continue
                # 工作路径
                work_path = re.sub('page_links', 'detail', parent)
                fp = open(full_filename, 'r', encoding='utf-8')
                text = fp.read()
                fp.close()
                json_data = json.loads(text)
                # 计数器
                self.counter[source] = (0, len(json_data))
                # 解析并yield
                for datum in json_data:
                    datum.update(path=work_path, category_code=category_code, source=source)
                    yield datum
                self.logger.info('File[%s] has loaded' % source)

    def create_request(self, datum):
        params = {'dbcode': datum['dbcode'], 'dbname': datum['dbname'], 'filename': datum['filename']}
        url = '%s?%s' % (self.base_url, urlencode(params))
        meta = {
            'path': datum['path'],
            'title': datum['title'],
            'category_code': datum['category_code'],
            'source': datum['source'],
            'max_retry_times': self.crawler.settings.get('MAX_RETRY_TIMES'),
            'publication_number': datum['filename'],
        }
        return Request(url=url, callback=self.parse, meta=meta)

    def parse(self, response):
        item = PatentItem()
        item['response'] = response
        item['title'] = response.meta['title']
        item['source'] = response.meta['source']
        item['category_code'] = response.meta['category_code']
        try:
            # 解析页面结构
            tr_list = response.xpath('//table[@id="box"]/tr')
            tr_index, tr_length = 0, len(tr_list)
            # 页面结构出现问题，报错
            if tr_length is 0:
                raise ValueError('not found table[@id="box"]')
            # 去掉最后一个tr 最后一个tr
            while tr_index < tr_length:
                td_list = tr_list[tr_index].xpath('./td')
                index, length, real_key = 0, len(td_list), None

                while index < length:
                    # 提取出文本
                    text = td_list[index].xpath('.//text()').extract_first().strip()
                    # 已经有key，则text为对应的value
                    if real_key:
                        item[real_key], real_key = text, None
                    # 过滤掉长度为0的键
                    elif len(text) > 0:
                        # 正则未提取到任何值 则键发生问题
                        result = re.search(self.pattern, text)
                        if result is None:
                            raise
                        key = result.group(1)
                        # 对应的键 没有则跳过下一个
                        if key in PatentItem.mapping:
                            real_key = PatentItem.mapping[key]
                        else:
                            index += 1
                    index += 1
                tr_index += 1
            yield item
            self.err_count = 0
        # 页面解析错误，重试
        except Exception as e:
            self.logger.error('%s %s页面解析出错: %s, 重试' % (response.meta['category_code'], response.meta['title'], e))
            # retry_times = response.meta.get('retry_times', 0) + 1
            # request = response.request.copy()
            # request.meta['retry_times'] = retry_times
            # yield request
            # 当出错超过5次后，则睡眠5min后再请求
            self.err_count += 1
            if self.err_count >= 5:
                self.err_count = 0
                self.logger.error('出错次数为%d，睡眠5分钟' % self.err_count)
                time.sleep(5 * 60)

