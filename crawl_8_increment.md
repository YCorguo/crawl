# 增量式爬虫
- 概念：监测网站数据更新的情况，只会爬取网站最新更新出来的数据。
- 分析：
    - 指定一个起始url
    - 基于CrawlSpider获取其他页码链接
    - 基于Rule将其他页码链接进行请求
    - 从每一个页码对应的页面源码中解析出每一个电影详情页的URL

    - 核心：检测电影详情页的url之前有没有请求过
        - 将爬取过的电影详情页的url存储
            - 存储到redis的set数据结构

    - 对详情页的url发起请求，然后解析出电影的名称和简介
    - 进行持久化存储
 
## 代码
见[moviePro](https://github.com/YCorguo/crawl/tree/main/moviePro)