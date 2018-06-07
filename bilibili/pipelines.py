# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymysql
from scrapy.conf import settings
import logging as logger
import time
from pymongo import MongoClient


class BilibiliPipeline(object):
    def __init__(self):
        # 建立数据库连接
        client = MongoClient(settings["MONGO_HOST"], settings["MONGO_PORT"])
        # 连接目标数据库
        db = client["bilibili"]
        db.authenticate(settings["MONGO_USERNAME"], settings["MONGO_PASSWORD"])
        # 连接集合
        # 根据当前日期建立集合
        col_name = "b_video_stat_" + time.strftime("%Y%m%d")
        col = db[col_name]

        self.col = col

    def process_item(self, item, spider):
        try:
            data = dict(item)
            self.col.insert_one(data)
        except Exception as error:
            # 记录保存错误的url
            logger.error(error)
            with open("./error_mongo.txt", "a") as fb:
                fb.write("aid:" + str(item["aid"]))
                fb.write("\n")
        return item

    # 保存到mysql
    # def process_item(self, item, spider):
    #     # 连接数据库
    #     connect = pymysql.connect(
    #         host=settings.MYSQL_HOST,
    #         db=settings.MYSQL_DBNAME,
    #         user=settings.MYSQL_USER,
    #         passwd=settings.MYSQL_PASSWD,
    #         charset='utf8mb4',
    #         use_unicode=True)
    #
    #     # 通过cursor执行增删查改
    #     cursor = connect.cursor()
    #     try:
    #         cursor.execute('''insert into b_video_stat(aid,view,danmaku,reply,favorite,coin,share)
    #                                 values (%d,%d,%d,%d,%d,%d,%d)''' % (item["aid"],
    #                                                                     item["view"],
    #                                                                     item["danmaku"],
    #                                                                     item["reply"],
    #                                                                     item["favorite"],
    #                                                                     item["coin"],
    #                                                                     item["share"]))
    #         # 提交sql语句
    #         connect.commit()
    #     except Exception as error:
    #         # 出现错误时打印错误日志
    #         logging.error((error, item))
    #
    #     connect.close()
    #     return item
