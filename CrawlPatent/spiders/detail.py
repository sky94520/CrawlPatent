# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
import random

from scrapy_splash import SplashRequest
from CrawlPatent.items import PatentItem


class DetailSpider(scrapy.Spider):
    name = 'detail'

    def __init__(self, queue, *args, **kwargs):
        self.queue = queue
        super().__init__(*args, **kwargs)

    def start_requests(self):
        script = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(args.wait))
            return splash:html()
        end
        """
        # url = 'http://dbpub.cnki.net/grid2008/dbpub/detail.aspx?dbcode=SCPD&dbname=SCPD2019&filename=CN110149756A'
        while len(self.queue) > 0:
            args = {
                'wait': random.randint(3, 6),
                'lua_source': script,
            }
            top = self.queue[0]
            self.queue.pop(0)
            url, title, path = top['url'], top['title'], top['path']

            yield SplashRequest(url, callback=self.parse, endpoint='execute', meta={'path': path, 'title': title}, args=args)

    def parse(self, response):
        item = PatentItem()
        item['response'] = response
        yield item

