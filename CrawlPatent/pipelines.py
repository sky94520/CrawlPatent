# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os

class CrawlpatentPipeline(object):
    def process_item(self, item, spider):
        return item


class SavePagePipeline(object):
    def process_item(self, item, spider):
        response = item['response']
        print(response.url)
        path = response.meta['path']
        title = response.meta['title']

        if not os.path.exists(path):
            os.makedirs(path)

        filename = os.path.join(path, '%s.html' % title)
        with open(filename, "wb") as fp:
            fp.write(response.body)


