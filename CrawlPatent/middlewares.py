# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import os
from urllib.parse import urlsplit, parse_qsl
import proxy_pool
from scrapy.http import Response
from scrapy_splash.response import SplashTextResponse
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import logging


logger = logging.getLogger(__name__)


class GetFromLocalityMiddleware(object):
    def process_request(self, request, spider):
        """
        尝试从本地获取源文件，如果存在，则直接获取
        :param request:
        :param spider:
        :return:
        """
        splash_url = spider.crawler.settings.get('SPLASH_URL')
        splash_result = urlsplit(splash_url)
        # 提取出code
        url = request.url
        result = urlsplit(url)
        # 不进行
        if result.scheme == splash_result.scheme and result.netloc == splash_result.netloc:
            return None

        tuple_list = parse_qsl(result.query)
        for key, value in tuple_list:
            if key == 'filename':
                filename = value
        # 文件存放位置
        path = request.meta['path']
        # 该路径存在该文件
        filepath = os.path.join(path, '%s.html' % filename)
        if os.path.exists(filepath):
            fp = open(filepath, 'rb')
            bytes = fp.read()
            fp.close()
            return SplashTextResponse(url=url, headers=request.headers, body=bytes, request=request)
        return None


class RetryOrErrorMiddleware(RetryMiddleware):
    """在之前的基础上增加了一条判断语句，当重试次数超过阈值时，发出错误"""

    def _retry(self, request, reason, spider):
        # 获取当前的重试次数
        retry_times = request.meta.get('retry_times', 0) + 1
        # 最大重试次数
        max_retry_times = self.max_retry_times
        if 'max_retry_times' in request.meta:
            max_retry_times = request.meta['max_retry_times']

        # 超出最大 直接报错即可
        if retry_times > max_retry_times:
            logger.error('%s %s retry times beyond the bounds' % (request.url, request.meta['title']))
        super()._retry(request, reason, spider)


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        # 最大重试次数
        retry_times = request.meta.get('retry_times', 0)
        max_retry_times = spider.crawler.settings.get('MAX_RETRY_TIMES')
        proxy = proxy_pool.get_random_proxy()
        # 最后一次尝试不使用代理
        if proxy and retry_times != max_retry_times:
            logger.info('使用代理%s' % proxy)
            request.meta['splash']['args']['proxy'] = 'http://%s' % proxy
        else:
            reason = '代理获取失败' if proxy else ('达到最大重试次数[%d/%d]' % (retry_times, max_retry_times))
            logger.warning('%s，使用自己的IP' % reason)

