# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import re
import json
import pymongo
import datetime
import logging
from scrapy.exceptions import DropItem


class FilterPipeline(object):
    """清除特殊字符"""
    def __init__(self):
        # 字符串转为数组
        self.array_keys = ['inventor', 'patent_cls_number', 'agent', 'applicant']
        # 字符串转为datetime
        self.date_keys = ['application_date', 'publication_date']
        # 去多个换行
        self.text_keys = ['sovereignty', 'summary']
        # 转成int
        self.int_keys = ['page_number']
        self.pattern = re.compile(r'\n+')

    def process_item(self, item, spider):
        for key, value in item.items():
            if key in self.array_keys:
                item[key] = value.split(';')
            elif key in self.date_keys:
                item[key] = datetime.datetime.strptime(value, '%Y-%m-%d')
            elif key in self.text_keys:
                item[key] = re.sub(self.pattern, '\n', value)
            elif key in self.int_keys:
                item[key] = int(value)
        if 'response' in item:
            del item['response']
        return item


class JsonPipeline(object):

    def process_item(self, item, spider):
        publication_number = item['publication_number']

        filename = os.path.join('%s.json' % publication_number)
        copy = dict(item.copy())
        del copy['response']
        with open(filename, "w", encoding='utf-8') as fp:
            fp.write(json.dumps(copy, ensure_ascii=False, indent=2))
        return item


class SavePagePipeline(object):
    def process_item(self, item, spider):
        response = item['response']

        path = response.meta['path']
        publication_number = item['publication_number']

        if not os.path.exists(path):
            os.makedirs(path)

        filename = os.path.join(path, '%s.html' % publication_number)
        with open(filename, "wb") as fp:
            fp.write(response.body)
        return item


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spdier):
        # 通过application_number保证唯一
        collection = self.db[item.collection]
        result = collection.find_one({'application_number': item['application_number']})
        if result is not None:
            raise DropItem()
        self.db[item.collection].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
