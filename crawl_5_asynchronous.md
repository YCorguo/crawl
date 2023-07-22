# 高性能异步爬虫
目的：在爬虫中使用异步实现高性能的数据爬取操作。

## 异步爬虫的方式：
1.多线程，多进程（不建议）：
    
- 好处：可以为相关阻塞的操作单独开启线程或者进程，阻塞操作就可以异步执行。

- 弊端：无法无限制的开启多线程或者多进程。

2.线程池、进程池（适当的使用）：
 
- 好处：我们可以降低系统对进程或者线程创建和销毁的一个频率，从而很好的降低系统的开销。

- 弊端：池中线程或进程的数量是有上限。

3.单线程+异步协程（推荐）：
    
- event_loop：事件循环，相当于一个无限循环，我们可以把一些函数注册到这个事件循环上，
当满足某些条件的时候，函数就会被循环执行。

- coroutine：协程对象，我们可以将协程对象注册到事件循环中，它会被事件循环调用。

- 我们可以使用 async 关键字来定义一个方法，这个方法在调用时不会立即被执行，而是返回
一个协程对象。

- task：任务，它是对协程对象的进一步封装，包含了任务的各个状态。

- future：代表将来执行或还没有执行的任务，实际上和 task 没有本质区别。

- async 定义一个协程.

- await 用来挂起阻塞方法的执行。

## 代码
### 同步爬虫
```
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
urls = [
    'http://xmdx.sc.chinaz.net/Files/DownLoad/jianli/201904/jianli10231.rar',
    'http://zjlt.sc.chinaz.net/Files/DownLoad/jianli/201904/jianli10229.rar',
    'http://xmdx.sc.chinaz.net/Files/DownLoad/jianli/201904/jianli10231.rar'
]

def get_content(url):
    print('正在爬取：',url)
    #get方法是一个阻塞的方法
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200 :
        return response.content

def parse_content(content):
    print('响应数据的长度为：',len(content))


for url in urls:
    content = get_content(url)
    parse_content(content)
```

### 线程池基本使用
```
# import time
# #使用单线程串行方式执行
#
# def get_page(str):
#     print("正在下载 ：",str)
#     time.sleep(2)
#     print('下载成功：',str)
#
# name_list =['xiaozi','aa','bb','cc']
#
# start_time = time.time()
#
# for i in range(len(name_list)):
#     get_page(name_list[i])
#
# end_time = time.time()
# print('%d second'% (end_time-start_time))
import time
#导入线程池模块对应的类
from multiprocessing.dummy import Pool
#使用线程池方式执行
start_time = time.time()
def get_page(str):
    print("正在下载 ：",str)
    time.sleep(2)
    print('下载成功：',str)

name_list =['xiaozi','aa','bb','cc']

#实例化一个线程池对象
pool = Pool(4)
#将列表中每一个列表元素传递给get_page进行处理。
pool.map(get_page,name_list)
pool.close()
pool.join()
end_time = time.time()
print(end_time-start_time)
```

### 线程池在爬虫案例中的应用
```
import requests
from lxml import etree
import re
from multiprocessing.dummy import Pool
#需求：爬取梨视频的视频数据
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
#原则：线程池处理的是阻塞且较为耗时的操作

#对下述url发起请求解析出视频详情页的url和视频的名称
url = 'https://www.pearvideo.com/category_5'
page_text = requests.get(url=url,headers=headers).text

tree = etree.HTML(page_text)
li_list = tree.xpath('//ul[@id="listvideoListUl"]/li')
urls = [] #存储所有视频的链接and名字
for li in li_list:
    detail_url = 'https://www.pearvideo.com/'+li.xpath('./div/a/@href')[0]
    name = li.xpath('./div/a/div[2]/text()')[0]+'.mp4'
    #对详情页的url发起请求
    detail_page_text = requests.get(url=detail_url,headers=headers).text
    #从详情页中解析出视频的地址（url）
    ex = 'srcUrl="(.*?)",vdoUrl'
    video_url = re.findall(ex,detail_page_text)[0]
    dic = {
        'name':name,
        'url':video_url
    }
    urls.append(dic)
#对视频链接发起请求获取视频的二进制数据，然后将视频数据进行返回
def get_video_data(dic):
    url = dic['url']
    print(dic['name'],'正在下载......')
    data = requests.get(url=url,headers=headers).content
    #持久化存储操作
    with open(dic['name'],'wb') as fp:
        fp.write(data)
        print(dic['name'],'下载成功！')
#使用线程池对视频数据进行请求（较为耗时的阻塞操作）
pool = Pool(4)
pool.map(get_video_data,urls)

pool.close()
pool.join()
```

### 协程
```
import asyncio

async def request(url):
    print('正在请求的url是',url)
    print('请求成功,',url)
    return url
#async修饰的函数，调用之后返回的一个协程对象
c = request('www.baidu.com')

# #创建一个事件循环对象
# loop = asyncio.get_event_loop()
#
# #将协程对象注册到loop中，然后启动loop
# loop.run_until_complete(c)

#task的使用
# loop = asyncio.get_event_loop()
# #基于loop创建了一个task对象
# task = loop.create_task(c)
# print(task)
#
# loop.run_until_complete(task)
#
# print(task)

#future的使用
# loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(c)
# print(task)
# loop.run_until_complete(task)
# print(task)

def callback_func(task):
    #result返回的就是任务对象中封装的协程对象对应函数的返回值
    print(task.result())

#绑定回调
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(c)
#将回调函数绑定到任务对象中
task.add_done_callback(callback_func)
loop.run_until_complete(task)
```

### 多任务协程
```
import asyncio
import time

async def request(url):
    print('正在下载',url)
    #在异步协程中如果出现了同步模块相关的代码，那么就无法实现异步。
    # time.sleep(2)
    #当在asyncio中遇到阻塞操作必须进行手动挂起
    await asyncio.sleep(2)
    print('下载完毕',url)

start = time.time()
urls = [
    'www.baidu.com',
    'www.sogou.com',
    'www.goubanjia.com'
]

#任务列表：存放多个任务对象
stasks = []
for url in urls:
    c = request(url)
    task = asyncio.ensure_future(c)
    stasks.append(task)

loop = asyncio.get_event_loop()
#需要将任务列表封装到wait中
loop.run_until_complete(asyncio.wait(stasks))

print(time.time()-start)
```

### 多任务异步协程
```
import requests
import asyncio
import time

start = time.time()
urls = [
    'http://127.0.0.1:5000/bobo','http://127.0.0.1:5000/jay','http://127.0.0.1:5000/tom'
]

async def get_page(url):
    print('正在下载',url)
    #requests.get是基于同步，必须使用基于异步的网络请求模块进行指定url的请求发送
    #aiohttp:基于异步网络请求的模块
    response = requests.get(url=url)
    print('下载完毕：',response.text)

tasks = []

for url in urls:
    c = get_page(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()

print('总耗时:',end-start)
```

### aiohttp实现多任务异步协程
```
#环境安装：pip install aiohttp
#使用该模块中的ClientSession
import requests
import asyncio
import time
import aiohttp

start = time.time()
# urls = [
#     'http://127.0.0.1:5000/bobo','http://127.0.0.1:5000/jay','http://127.0.0.1:5000/tom',
#     'http://127.0.0.1:5000/bobo', 'http://127.0.0.1:5000/jay', 'http://127.0.0.1:5000/tom',
#     'http://127.0.0.1:5000/bobo', 'http://127.0.0.1:5000/jay', 'http://127.0.0.1:5000/tom',
#     'http://127.0.0.1:5000/bobo', 'http://127.0.0.1:5000/jay', 'http://127.0.0.1:5000/tom',
#
# ]
from multiprocessing.dummy import Pool
pool = Pool(2)

urls = []
for i in range(10):
    urls.append('http://127.0.0.1:5000/bobo')
print(urls)
async def get_page(url):
    async with aiohttp.ClientSession() as session:
        #get()、post():
        #headers,params/data,proxy='http://ip:port'
        async with await session.get(url) as response:
            #text()返回字符串形式的响应数据
            #read()返回的二进制形式的响应数据
            #json()返回的就是json对象
            #注意：获取响应数据操作之前一定要使用await进行手动挂起
            page_text = await response.text()
            print(page_text)

tasks = []

for url in urls:
    c = get_page(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait(tasks))

end = time.time()

print('总耗时:',end-start)
```

### 多任务异步协程+1
```
import requests
from lxml import etree
import time
import os
start = time.time()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
if not os.path.exists('./libs'):
    os.mkdir('./libs')
url = 'http://pic.netbian.com/4kmeinv/index_%d.html'
a = []
for page in range(2,50):
    new_url = format(url%page)
    page_text = requests.get(url=new_url,headers=headers).text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//div[@class="slist"]/ul/li')
    for li in li_list:
        img_src = 'http://pic.netbian.com' + li.xpath('./a/img/@src')[0]
        name = img_src.split('/')[-1]
        # data = requests.get(url=img_src).content
        # path = './libs/'+name
        # with open(path,'wb') as fp:
        #     fp.write(data)
        #     print(name,'下载成功')
        a.append(name)
print(len(a))
print('总耗时：',time.time()-start)
```

### flask服务
```
from flask import Flask
import time

app = Flask(__name__)


@app.route('/bobo')
def index_bobo():
    time.sleep(2)
    return 'Hello bobo'

@app.route('/jay')
def index_jay():
    time.sleep(2)
    return 'Hello jay'

@app.route('/tom')
def index_tom():
    time.sleep(2)
    return 'Hello tom'

if __name__ == '__main__':
    app.run(threaded=True)
```
