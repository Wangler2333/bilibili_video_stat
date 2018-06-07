# bilibili_video_stat
爬取b站视频信息，供大数据分析用户喜好。使用scrapy-redis分布式，在16核服务器上实现抓取2500万条/天。可长期部署抓取，实现视频趋势分析

- 1.提供代理ip池
- 2.提供user agent池
- 3.使用scrapy-redis分布式
- 4.使用mongodb保存数据（也可使用mysql，提供了相应代码）
- 5.使用多进程（单个爬虫线程数请根据设备情况自行在settings.py中修改）
- 6.提供完整error记录
- 7.提供自定义重试中间件UserRetryMiddleware（如使用，请在settings.py中修改）

### 启动命令

```shell
pip3 install -r requirements.txt
python3 start.py 进程数
# python3 start.py 32
```

- 建议配合代理ip池使用，提供 https://github.com/arthurmmm/hq-proxies 代理池的调用中间件，需在settings中开启中间件

- 请在使用前设置settings.py中的redis和mongodb的连接

- pipeline.py注释了使用mysql保存的代码，如使用，请在settings.py添加相应设置
