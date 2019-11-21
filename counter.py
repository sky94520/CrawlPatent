import os
import pprint
import json
from collections import Counter
from MongoDB import MongoDB
from config import MONGODB_CONFIG


basedir = os.path.realpath(os.path.dirname(__file__))
detail_path = os.path.join(basedir, 'files', 'detail')


if __name__ == '__main__':
    companies = []
    # 遍历整个page_links文件夹
    for parent, dirnames, filenames in os.walk(detail_path, followlinks=True):
        company = os.path.split(parent)[-1]
        # 遍历所有的文件 统计出每个公司的专利号
        patents = []
        for filename in filenames:
            publication_number = os.path.splitext(filename)[0]
            patents.append(publication_number)
        if len(patents) != 0:
            companies.append({'name': company, 'patents': patents})
    print(companies)
    # 查询mongodb
    mongo = MongoDB(host=MONGODB_CONFIG['ip'], port=MONGODB_CONFIG['port'])
    mongo.authenticate('admin', MONGODB_CONFIG['username'], MONGODB_CONFIG['password'])
    patent_db = mongo.get_db('patent')
    collection = patent_db['invention_patent']
    # 保存到文件中
    fp = open('result.csv', 'w', encoding='utf-8')
    # 遍历 统计
    for company in companies:
        company_name = company['name']
        application_numbers = company['patents']
        # 查询
        filter_names = {'_id': 0, 'publication_number': 1, 'main_cls_number': 1}
        generator = collection.find({'publication_number': {'$in': application_numbers}}, filter_names)
        counter = Counter()
        for patent in generator:
            cls_number = patent['main_cls_number']
            # 取前面
            # index = cls_number.find('/')
            # cls_number = cls_number[:index]

            counter[cls_number] = counter[cls_number] + 1
        if len(counter) != 0:
            cls_number = None
            count = 0
            for key, value in counter.items():
                if cls_number is None or count < value:
                    cls_number = key
                    count = value
            print(company_name, cls_number)
            fp.write('%s,%s\n' % (company_name, cls_number))
    fp.close()

