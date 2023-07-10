# -*- coding:utf-8 -*-

# 导入必要包
import requests
import json

# 目录
# 1. 直接发送请求：requests.get()
# 2. 进行UA伪装：headers
# 3. 抓包获取ajax数据：requests.post()
# 4. 循环爬取数据：for


#- 需求1：爬取搜狗首页的页面数据
# 方式：直接发送请求。
#step_1:指定url
url = 'https://www.sogou.com/'
#step_2:发起请求
#get方法会返回一个响应对象
response = requests.get(url=url)
#step_3:获取响应数据.text返回的是字符串形式的响应数据
page_text = response.text
print(page_text)
#step_4:持久化存储
with open('./sogou.html','w',encoding='utf-8') as fp:
    fp.write(page_text)
print('爬取数据结束！！！')

#- 需求2：爬取搜狗搜索某关键词的页面数据
# 方式：进行UA伪装
#UA：User-Agent（请求载体的身份标识）
#UA检测：门户网站的服务器会检测对应请求的载体身份标识，如果检测到请求的载体身份标识为某一款浏览器，
#说明该请求是一个正常的请求。但是，如果检测到请求的载体身份标识不是基于某一款浏览器的，则表示该请求
#为不正常的请求（爬虫），则服务器端就很有可能拒绝该次请求。

#UA伪装：让爬虫对应的请求载体身份标识伪装成某一款浏览器
#UA伪装：将对应的User-Agent封装到一个字典中
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
url = 'https://www.sogou.com/web'
#处理url携带的参数：封装到字典中
kw = input('enter a word:')
param = {
    'query':kw
}
#对指定的url发起的请求对应的url是携带参数的，并且请求过程中处理了参数
response = requests.get(url=url,params=param,headers=headers)

page_text = response.text
fileName = kw+'.html'
with open(fileName,'w',encoding='utf-8') as fp:
    fp.write(page_text)
print(fileName,'保存成功！！！')


#- 需求3：爬取百度翻译某关键词的页面数据。
# 方式：抓包获取ajax数据。
#1.指定url
post_url = 'https://fanyi.baidu.com/sug'
#2.进行UA伪装
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

}
#3.post请求参数处理（同get请求一致）
word = input('enter a word:')
data = {
    'kw':word
}
#4.请求发送
response = requests.post(url=post_url,data=data,headers=headers)
#5.获取响应数据:json()方法返回的是obj（如果确认响应数据是json类型的，才可以使用json（））
dic_obj = response.json()

#持久化存储
fileName = word+'.json'
fp = open(fileName,'w',encoding='utf-8')
json.dump(dic_obj,fp=fp,ensure_ascii=False)

print('over!!!')

#- 需求4：爬取豆瓣电影信息
# 方式：循环爬取数据。
url = 'https://movie.douban.com/j/chart/top_list'

list_data = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

}

for start in range(0, 100, 20):
    param = {
        'type': '24',
        'interval_id': '100:90',
        'action':'',
        'start': str(start),#从库中的第几部电影去取
        'limit': '20',#一次取出的个数
    }
    response = requests.get(url=url,params=param,headers=headers)

    list_data += response.json()

fp = open('./douban.json','w',encoding='utf-8')
json.dump(list_data,fp=fp,ensure_ascii=False)
print('over!!!')
