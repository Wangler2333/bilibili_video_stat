#!/usr/bin/env python
# encoding: utf-8 
# @version: 
# @author: liduo
# @license: 
# @file: redis_n.py
# @time: 2018/5/30 下午5:05
from redis import StrictRedis
import settings
from concurrent.futures import ThreadPoolExecutor


def run(t):
    # 向redis传入strat_urls
    start = t[0]
    stop = t[1]
    redis_db = StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=0,
    )

    for i in range(start, stop):
        print(i)

        redis_db.lpush("bilibili_spider:strat_urls", "https://api.bilibili.com/x/web-interface/archive/stat?aid=%s" % i)


def main(start, stop, step):
    # 开启多线程
    num_list = []
    # 为每个线程分配aid，组成列表
    for i in range(start, stop, step):
        start_i = i
        stop_i = i + step
        t = (start_i, stop_i)
        num_list.append(t)
    # 设置线程池大小，或动态生成大小
    pool_num = 32
    # pool_num = (stop - start) // step
    with ThreadPoolExecutor(pool_num) as executor:
        # 使用map动态生成线程
        executor.map(run, num_list)


if __name__ == '__main__':
    import sys

    # 接收参数，start，stop，step
    # start：起始aid
    # stop：结束aid
    # step：每个线程负责aid的数量
    start_num = int(sys.argv[1])
    stop_num = int(sys.argv[2])
    step_num = int(sys.argv[3])
    main(start_num, stop_num, step_num)
