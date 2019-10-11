# -*- coding: utf-8 -*-

# Scrapy settings for CrawlPatent project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import logging
import datetime

BOT_NAME = 'CrawlPatent'

SPIDER_MODULES = ['CrawlPatent.spiders']
NEWSPIDER_MODULE = 'CrawlPatent.spiders'

BASEDIR = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'CrawlPatent (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 最大重试次数
MAX_RETRY_TIMES = 20
# mongo数据库相关
MONGO_URI = 'mongodb://root:qwerty1234@47.107.246.172:27017/admin'
MONGO_DB = 'patent'
# redis的相关配置
REDIS_CONFIG = {
    'host': '47.107.246.172',
    'port': 6379,
    'password': None,
}

# 配置Splash
SPLASH_URL = 'http://47.107.246.172:8050'
# 去重
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# 配置Cache存储
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# 日志格式化输出
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# 日期格式
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
NAME_FORMAT = "%H-%M-%S"

now = datetime.datetime.now()
filepath = os.path.join(BASEDIR, 'log', now.strftime("%Y-%m-%d"))

if not os.path.exists(filepath):
    os.makedirs(filepath)
# 仅仅把错误及其以上存入文件
filename = os.path.join(filepath, "%s.txt" % now.strftime("%H-%M-%S"))
fp = logging.FileHandler(filename, "w", encoding="utf-8")
fp.setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp])

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'CrawlPatent.middlewares.GetFromLocalityMiddleware': 543,
    'CrawlPatent.middlewares.RetryOrErrorMiddleware': 550,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'CrawlPatent.middlewares.ProxyMiddleware': 843,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'CrawlPatent.pipelines.SavePagePipeline': 300,
    'CrawlPatent.pipelines.FilterPipeline': 301,
    'CrawlPatent.pipelines.MongoPipeline': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
