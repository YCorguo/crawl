### 编码规则
```
# -*- coding:utf-8 -*-
```
### 导入必要包
```
import requests
import re
import os
from bs4 import BeautifulSoup
from lxml import etree
```

### 目录
1. 爬取图片数据。
2. 正则解析式。
3. 分页爬取。
4. bs4解析本地文件。
5. bs4解析爬取数据。
6. xpath解析本地文件。
7. xpath解析爬取数据。
8. 解决中文乱码问题。
9. xpath综合爬取（管道符号｜）。

### 需求1:爬取图片数据
```
url = 'https://pic.qiushibaike.com/system/pictures/12172/121721055/medium/9OSVY4ZSU4NN6T7V.jpg'
#content返回的是二进制形式的图片数据
# text（字符串） content（二进制）json() (对象)
img_data = requests.get(url=url).content

with open('./qiutu.jpg','wb') as fp:
    fp.write(img_data)
```


### 需求2：爬取糗事百科中糗图板块下所有的糗图图片
```
#创建一个文件夹，保存所有的图片
if not os.path.exists('./qiutuLibs'):
    os.mkdir('./qiutuLibs')

url = 'https://www.qiushibaike.com/pic/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

}
#使用通用爬虫对url对应的一整张页面进行爬取
page_text = requests.get(url=url,headers=headers).text

#使用聚焦爬虫将页面中所有的糗图进行解析/提取
ex = '<div class="thumb">.*?<img src="(.*?)" alt.*?</div>'
img_src_list = re.findall(ex,page_text,re.S)
# print(img_src_list)
for src in img_src_list:
    #拼接出一个完整的图片url
    src = 'https:'+src
    #请求到了图片的二进制数据
    img_data = requests.get(url=src,headers=headers).content
    #生成图片名称
    img_name = src.split('/')[-1]
    #图片存储的路径
    imgPath = './qiutuLibs/'+img_name
    with open(imgPath,'wb') as fp:
        fp.write(img_data)
        print(img_name,'下载成功！！！')
```

### 需求3：分页爬取糗事百科中糗图板块下所有的糗图图片
```
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

}
#创建一个文件夹，保存所有的图片
if not os.path.exists('./qiutuLibs'):
    os.mkdir('./qiutuLibs')
#设置一个通用的url模板
url = 'https://www.qiushibaike.com/pic/page/%d/?s=5184961'
# pageNum = 2

for pageNum in range(1,3):
    #对应页码的url
    new_url = format(url%pageNum)


    #使用通用爬虫对url对应的一整张页面进行爬取
    page_text = requests.get(url=new_url,headers=headers).text

    #使用聚焦爬虫将页面中所有的糗图进行解析/提取
    ex = '<div class="thumb">.*?<img src="(.*?)" alt.*?</div>'
    img_src_list = re.findall(ex,page_text,re.S)
    # print(img_src_list)
    for src in img_src_list:
        #拼接出一个完整的图片url
        src = 'https:'+src
        #请求到了图片的二进制数据
        img_data = requests.get(url=src,headers=headers).content
        #生成图片名称
        img_name = src.split('/')[-1]
        #图片存储的路径
        imgPath = './qiutuLibs/'+img_name
        with open(imgPath,'wb') as fp:
            fp.write(img_data)
            print(img_name,'下载成功！！！')
```


### 需求4: 将本地的html文档中的数据加载到该对象中
```
fp = open('./test.html','r',encoding='utf-8')
soup = BeautifulSoup(fp,'lxml')
# print(soup)
# print(soup.a) #soup.tagName 返回的是html中第一次出现的tagName标签
# print(soup.div)
#find('tagName'):等同于soup.div
# print(soup.find('div'))  #print(soup.div)
# print(soup.find('div',class_='song').string)
# print(soup.find_all('a'))
# print(soup.select('.tang'))
print(soup.select('.tang > ul a')[0]['href'])
```

### 需求5：爬取三国演义小说所有的章节标题和章节内容
```
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
url = 'http://www.shicimingju.com/book/sanguoyanyi.html'
page_text = requests.get(url=url,headers=headers).text

#在首页中解析出章节的标题和详情页的url
#1.实例化BeautifulSoup对象，需要将页面源码数据加载到该对象中
soup = BeautifulSoup(page_text,'lxml')
#解析章节标题和详情页的url
li_list = soup.select('.book-mulu > ul > li')
fp = open('./sanguo.txt','w',encoding='utf-8')
for li in li_list:
    title = li.a.string
    detail_url = 'http://www.shicimingju.com'+li.a['href']
    #对详情页发起请求，解析出章节内容
    detail_page_text = requests.get(url=detail_url,headers=headers).text
    #解析出详情页中相关的章节内容
    detail_soup = BeautifulSoup(detail_page_text,'lxml')
    div_tag = detail_soup.find('div',class_='chapter_content')
    #解析到了章节的内容
    content = div_tag.text
    fp.write(title+':'+content+'\n')
    print(title,'爬取成功！！！')
```

### 需求6: 实例化好了一个etree对象，且将被解析的源码加载到了该对象中
```
tree = etree.parse('test.html')
# r = tree.xpath('/html/body/div')
# r = tree.xpath('/html//div')
# r = tree.xpath('//div')
# r = tree.xpath('//div[@class="song"]')
# r = tree.xpath('//div[@class="tang"]//li[5]/a/text()')[0]
# r = tree.xpath('//li[7]//text()')
# r = tree.xpath('//div[@class="tang"]//text()')
r = tree.xpath('//div[@class="song"]/img/@src')
print(r)
```

### 需求7：爬取58二手房中的房源信息
```
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
#爬取到页面源码数据
url = 'https://bj.58.com/ershoufang/'
page_text = requests.get(url=url,headers=headers).text

#数据解析
tree = etree.HTML(page_text)
#存储的就是li标签对象
li_list = tree.xpath('//ul[@class="house-list-wrap"]/li')
fp = open('58.txt','w',encoding='utf-8')
for li in li_list:
    #局部解析
    title = li.xpath('./div[2]/h2/a/text()')[0]
    print(title)
    fp.write(title+'\n')
```

### 需求8：解析下载图片数据
```
url = 'http://pic.netbian.com/4kmeinv/'
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
response = requests.get(url=url,headers=headers)
#手动设定响应数据的编码格式
# response.encoding = 'utf-8'
page_text = response.text

#数据解析：src的属性值  alt属性
tree = etree.HTML(page_text)
li_list = tree.xpath('//div[@class="slist"]/ul/li')


#创建一个文件夹
if not os.path.exists('./picLibs'):
    os.mkdir('./picLibs')

for li in li_list:
    img_src = 'http://pic.netbian.com'+li.xpath('./a/img/@src')[0]
    img_name = li.xpath('./a/img/@alt')[0]+'.jpg'
    #通用处理中文乱码的解决方案
    img_name = img_name.encode('iso-8859-1').decode('gbk')

    # print(img_name,img_src)
    #请求图片进行持久化存储
    img_data = requests.get(url=img_src,headers=headers).content
    img_path = 'picLibs/'+img_name
    with open(img_path,'wb') as fp:
        fp.write(img_data)
        print(img_name,'下载成功！！！')
```

### 需求9：解析出所有城市名称
```
# headers = {
#     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
# }
# url = 'https://www.aqistudy.cn/historydata/'
# page_text = requests.get(url=url,headers=headers).text
#
# tree = etree.HTML(page_text)
# host_li_list = tree.xpath('//div[@class="bottom"]/ul/li')
# all_city_names = []
# #解析到了热门城市的城市名称
# for li in host_li_list:
#     hot_city_name = li.xpath('./a/text()')[0]
#     all_city_names.append(hot_city_name)
#
# #解析的是全部城市的名称
# city_names_list = tree.xpath('//div[@class="bottom"]/ul/div[2]/li')
# for li in city_names_list:
#     city_name = li.xpath('./a/text()')[0]
#     all_city_names.append(city_name)
#
# print(all_city_names,len(all_city_names))

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
url = 'https://www.aqistudy.cn/historydata/'
page_text = requests.get(url=url, headers=headers).text

tree = etree.HTML(page_text)
#解析到热门城市和所有城市对应的a标签
# //div[@class="bottom"]/ul/li/          热门城市a标签的层级关系
# //div[@class="bottom"]/ul/div[2]/li/a  全部城市a标签的层级关系
a_list = tree.xpath('//div[@class="bottom"]/ul/li/a | //div[@class="bottom"]/ul/div[2]/li/a')
all_city_names = []
for a in a_list:
    city_name = a.xpath('./text()')[0]
    all_city_names.append(city_name)
print(all_city_names,len(all_city_names))
```
