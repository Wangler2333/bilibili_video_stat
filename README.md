# bilibili_video_stat
爬取b站视频信息，供大数据分析用户喜好。使用scrapy-redis分布式，在16核服务器上实现抓取2500万条/天。可长期部署抓取，实现视频趋势分析

- 1.提供代理ip池
- 2.提供user agent池
- 3.使用scrapy-redis分布式
- 4.使用mongodb保存数据（也可使用mysql，提供了相应代码）
- 5.使用多进程（单个爬虫线程数请根据设备情况自行在settings.py中修改）
- 6.提供完整error记录
- 7.提供自定义重试中间件UserRetryMiddleware（如使用，请在settings.py中修改）
- 8.提供在redis中添加starurls的代码，请阅读redis_n.py文件

### 启动命令

```shell
pip3 install -r requirements.txt
python3 start.py 进程数
# python3 start.py 32
```

- 建议配合代理ip池使用，提供 https://github.com/arthurmmm/hq-proxies 代理池的调用中间件，需在settings中开启中间件

- 请在使用前设置settings.py中的redis和mongodb的连接

- pipeline.py注释了使用mysql保存的代码，如使用，请在settings.py添加相应设置

## 千万级大数据量/天的爬取经验：

- 1.请准备较大的代理IP池：若数据量在400条/秒，根据b站封ip的测试（短时间请求1000次则封ip），代理池需维持300-400的代理ip

- 2.请使用短有效期的代理ip：代理ip有效期在3-5分钟需300-400的代理池IP量，若有效期较长，需增加代理池的ip量

- 3.请准备较多的user agent组成池，useragent.py中的量差不多了

- 4.请开启重试：超时时间调小为10s，重试次数增加为10；实际测试中，重试1次约占30%，重试2次及以上约占10%，最多的重试了6次；重试占比于代理ip质量相关

- 5.若出现所有请求全部都重试的情况，请开启DOWNLOAD_DELAY = 0.01；实际测试，即使只延迟0.01s也会显著减少重试次数；若重试情况仍严重，请增加至0.25s

- 6.需详细记录失败的url，保持数据的完整性
