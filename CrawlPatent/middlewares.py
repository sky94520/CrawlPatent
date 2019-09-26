# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import proxy_pool
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import logging


logger = logging.getLogger(__name__)


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
        max_retry_times = spider.crawler.settings.get('MAX_RETRY_TIMES')
        proxy = proxy_pool.get_random_proxy()
        # 最后一次尝试不使用代理
        if proxy and ('retry_times' not in request.meta or request.meta['retry_times'] == max_retry_times):
            logger.info('使用代理%s' % proxy)
            request.meta['splash']['args']['proxy'] = proxy
        else:
            logger.warning('代理获取失败，使用自己的IP')

