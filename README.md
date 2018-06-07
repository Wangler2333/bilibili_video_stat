# bilibili_video_stat
爬取b站视频信息，供大数据分析用户喜好。使用scrapy-redis分布式，在16核服务器上实现抓取2500万条/天。可长期部署抓取，实现视频趋势分析

### 启动命令

```shell
pip3 install -r requirements.txt
python3 start.py 进程数
# python3 start.py 32
```
