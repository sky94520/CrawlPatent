# -*- coding: utf-8 -*-
import scrapy
import os
import re
import json
import time
from urllib.parse import quote
import random
import redis

from scrapy_splash import SplashRequest
from CrawlPatent.items import PatentItem


class DetailSpider(scrapy.Spider):
    name = 'detail'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        REDIS_CONFIG = crawler.settings.get('REDIS_CONFIG')
        spider = cls(REDIS_CONFIG, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def __init__(self, redis_config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = redis.StrictRedis(**redis_config, decode_responses=True)
        self.script = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(args.wait))
            return splash:html()
        end
        """

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
                # 判断该文件是否已经访问过了
                real_name = '%s/%s' % (category_code, filename)
                if self.db.sismember('page_links', real_name):
                    continue
                self.db.sadd('page_links', real_name)
                # 工作路径
                work_path = re.sub('page_links', 'detail', parent)
                fp = open(full_filename, 'r', encoding='utf-8')
                text = fp.read()
                fp.close()

                json_data = json.loads(text)
                for datum in json_data:
                    datum['path'] = work_path
                    datum['category_code'] = category_code
                    yield datum
                # TODO:当前仅仅返回一个
                return

    def create_request(self, top):
        args = {
            'wait': random.randint(3, 6),
            'lua_source': self.script,
        }
        meta = {
            'path': top['path'],
            'title': top['title'],
            'category_code': top['category_code'],
            'max_retry_times': self.crawler.settings.get('MAX_RETRY_TIMES')
        }
        return SplashRequest(top['url'], callback=self.parse, endpoint='execute',
                             meta=meta, args=args)

    def parse(self, response):
        item = PatentItem()
        item['response'] = response
        item['title'] = response.meta['title']
        item['category_code'] = response.meta['category_code']
        try:
            # 解析页面结构
            data = response.css('#box').css('td[bgcolor="#FFFFFF"]::text').extract()
            data = [datum.strip() for datum in data if len(datum.strip()) > 0]
            item['application_number'] = data[0]
            item['application_date'] = data[1]
            item['publication_number'] = data[2]
            item['publication_date'] = data[3]
            item['applicant'] = data[4]
            item['address'] = data[5]
            item['inventor'] = data[6]
            item['agency'] = data[7]
            item['agent'] = data[8]
            item['code'] = data[9]
            item['summary'] = data[10]
            item['sovereignty'] = data[11]
            item['page_number'] = data[12]
            item['main_cls_number'] = data[13]
            item['patent_cls_number'] = data[14]
            yield item
        # 页面解析错误，重试
        except Exception as e:
            self.logger.error('%s %s页面解析出错: %s, 重试' % (response['category_code'], response['title'], e))
            retry_times = response.meta.get('retry_times', 0) + 1
            request = response.request.copy()
            request.meta['retry_times'] = retry_times
            yield request

