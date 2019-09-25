import os
import re
import json
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 保存的路径
# 队列
queue = []


def run():
    # 爬取使用的spider名称
    spider_name = 'detail'
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    # 合并配置
    process = CrawlerProcess(settings)
    # 启动爬虫
    process.crawl(spider_name, **{'queue': queue})
    process.start()


def main():
    path = os.path.join(basedir, 'files', 'page_links')

    for parent, dirnames, filenames in os.walk(path, followlinks=True):
        print(parent)
        for filename in filenames:
            full_filename = os.path.join(parent, filename)
            # 工作路径
            work_path = re.sub('page_links', 'detail', parent)
            fp = open(full_filename, 'r', encoding='utf-8')
            text = fp.read()
            fp.close()

            json_data = json.loads(text)
            for datum in json_data:
                datum['path'] = work_path
                print(datum)
                queue.append(datum)

            run()
            return
            # print('文件完整路径 %s' % filepath)


if __name__ == '__main__':
    # run()
    main()
