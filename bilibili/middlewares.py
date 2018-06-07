# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from redis import StrictRedis
from scrapy.conf import settings
from scrapy import signals
import random  # 随机选择
from .useragent import agents  # 导入前面的
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware  # UserAegent中间件
from scrapy.downloadermiddlewares.retry import RetryMiddleware  # 重写重试中间件


class UserRetryMiddleware(RetryMiddleware):
    # 自定义重试中间件，未启用
    def _retry(self, request, reason, spider):
        redis_db = StrictRedis(
            host=settings["REDIS_HOST"],
            port=settings["REDIS_PORT"],
            password=settings["REDIS_PASSWORD"],
            db=settings["REDIS_PROXY_DB"],
        )
        print(request.url)
        redis_db.lpush("bilibili_spider:strat_urls", request.url)


class UserAgentmiddleware(UserAgentMiddleware):
    # 随机user agent的中间件
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class BilibiliDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.spider_error, signal=signals.spider_error)
        return s

    def process_request(self, request, spider):
        # 使用代理ip池的中间件
        # 配合https://github.com/arthurmmm/hq-proxies使用
        # 若使用请在settings中开启
        redis_db = StrictRedis(
            host=settings["REDIS_HOST"],
            port=settings["REDIS_PORT"],
            password=settings["REDIS_PASSWORD"],
            db=settings["REDIS_PROXY_DB"],
        )

        proxy = redis_db.srandmember("hq-proxies:proxy_pool", 1)
        if proxy:
            proxy = proxy[0].decode()
            spider.logger.info('使用代理[%s]访问[%s]' % (proxy, request.url))

            request.meta['proxy'] = proxy
        else:
            spider.logger.warning('不使用代理访问[%s]' % request.url)
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('爬虫开启: %s' % spider.name)

    def spider_closed(self, spider):
        spider.logger.info('爬虫关闭: %s' % spider.name)

    def spider_error(self, failure, response, spider):
        # 增加记录爬虫报错的函数，连接spider_error信号
        spider.logger.error('[%s],错误:%s' % (response.url, failure.getTraceback()))
        with open("./error_spider.txt", "a") as fa:
            fa.write(response.url)
            fa.write("\n")
        with open("./error_spider_info.txt", "a") as fb:
            fb.write("Error on {0}, traceback: {1}".format(response.url, failure.getTraceback()))
            fb.write("\n")
