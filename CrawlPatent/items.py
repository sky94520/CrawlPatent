# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PatentItem(scrapy.Item):
    # 集合名称
    collection = 'patent'
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 保存response
    response = scrapy.Field()
    # 类别代码
    category_code = scrapy.Field()
    # 专利名
    title = scrapy.Field()
    # 申请号
    application_number = scrapy.Field()
    # 申请日
    application_date = scrapy.Field()
    # 公开号
    publication_number = scrapy.Field()
    # 公开日
    publication_date = scrapy.Field()
    # 申请人
    applicant = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 发明人
    inventor = scrapy.Field()
    # 代理机构
    agency = scrapy.Field()
    # 代理人
    agent = scrapy.Field()
    # 国省代码
    code = scrapy.Field()
    # 摘要
    summary = scrapy.Field()
    # 主权项
    sovereignty = scrapy.Field()
    # 页数
    page_number = scrapy.Field()
    # 主分类号
    main_cls_number = scrapy.Field()
    # 专利分类号
    patent_cls_number = scrapy.Field()
