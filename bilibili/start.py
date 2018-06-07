#!/usr/bin/env python
# encoding: utf-8 
# @version: 
# @author: liduo
# @license: 
# @file: start.py
# @time: 2018/5/30 下午10:24
from multiprocessing import Pool
import os


def run():
    # 发送命令，启动一个爬虫
    cmd = "scrapy crawl bilibili_spider"
    os.system(cmd)


def main(number):
    # 创建进程池
    p = Pool(number)
    for n in range(number):
        p.apply_async(run)
    p.close()
    p.join()


if __name__ == '__main__':
    import sys

    # 接收传入的参数，代表开启几个scrapy-redis进程
    num = sys.argv[1]
    num = int(num)
    print("开启[%s]个进程" % num)
    main(num)
    print("进程结束")
