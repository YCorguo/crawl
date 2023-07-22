# selenium模块的基本使用

## 问题：selenium模块和爬虫之间具有怎样的关联？
- 便捷的获取网站中动态加载的数据
- 便捷实现模拟登录

## 什么是selenium模块？
- 基于浏览器自动化的一个模块。

## selenium使用流程：
- 环境安装：pip install selenium
- 下载一个浏览器的驱动程序（谷歌浏览器）
    - 下载路径：http://chromedriver.storage.googleapis.com/index.html
    - 驱动程序和浏览器的映射关系：http://blog.csdn.net/huilan_same/article/details/51896672
- 实例化一个浏览器对象
- 编写基于浏览器自动化的操作代码
    - 发起请求：get(url)
    - 标签定位：find系列的方法
    - 标签交互：send_keys('xxx')
    - 执行js程序：excute_script('jsCode')
    - 前进，后退：back(),forward()
    - 关闭浏览器：quit()

- selenium处理iframe
    - 如果定位的标签存在于iframe标签之中，则必须使用switch_to.frame(id)
    - 动作链（拖动）：from selenium.webdriver import ActionChains
        - 实例化一个动作链对象：action = ActionChains(bro)
        - click_and_hold（div）：长按且点击操作
        - move_by_offset(x,y)
        - perform()让动作链立即执行
        - action.release()释放动作链对象

## 12306模拟登录
- 超级鹰：http://www.chaojiying.com/about.html
    - 注册：普通用户
    - 登录：普通用户
        - 题分查询：充值
        - 创建一个软件（id）
        - 下载示例代码

- 12306模拟登录编码流程：
    - 使用selenium打开登录页面
    - 对当前selenium打开的这张页面进行截图
    - 对当前图片局部区域（验证码图片）进行裁剪
        - 好处：将验证码图片和模拟登录进行一一对应。
    - 使用超级鹰识别验证码图片（坐标）
    - 使用动作链根据坐标实现点击操作
    - 录入用户名密码，点击登录按钮实现登录

## 代码
### 演示程序
```
from selenium import webdriver
from time import sleep
# 后面是你的浏览器驱动位置，记得前面加r'','r'是防止字符转义的
driver = webdriver.Chrome(r'./chromedriver')
# 用get打开百度页面
driver.get("http://www.baidu.com")
# 查找页面的“设置”选项，并进行点击
driver.find_elements_by_link_text('设置')[0].click()
sleep(2)
# # 打开设置后找到“搜索设置”选项，设置为每页显示50条
driver.find_elements_by_link_text('搜索设置')[0].click()
sleep(2)
# 选中每页显示50条
m = driver.find_element_by_id('nr')
sleep(2)
m.find_element_by_xpath('//*[@id="nr"]/option[3]').click()
m.find_element_by_xpath('.//option[3]').click()
sleep(2)
# 点击保存设置
driver.find_elements_by_class_name("prefpanelgo")[0].click()
sleep(2)
# 处理弹出的警告页面   确定accept() 和 取消dismiss()
driver.switch_to_alert().accept()
sleep(2)
# 找到百度的输入框，并输入 美女
driver.find_element_by_id('kw').send_keys('美女')
sleep(2)
# 点击搜索按钮
driver.find_element_by_id('su').click()
sleep(2)
# 在打开的页面中找到“Selenium - 开源中国社区”，并打开这个页面
driver.find_elements_by_link_text('美女_百度图片')[0].click()
sleep(3)
# 关闭浏览器
driver.quit()
```

### selenium基础用法
```
from selenium import webdriver
from lxml import etree
from time import sleep
#实例化一个浏览器对象（传入浏览器的驱动成）
bro = webdriver.Chrome(executable_path='./chromedriver')
#让浏览器发起一个指定url对应请求
bro.get('http://125.35.6.84:81/xk/')

#page_source获取浏览器当前页面的页面源码数据
page_text = bro.page_source

#解析企业名称
tree = etree.HTML(page_text)
li_list = tree.xpath('//ul[@id="gzlist"]/li')
for li in li_list:
    name = li.xpath('./dl/@title')[0]
    print(name)
sleep(5)
bro.quit()
```

### selenium其他自动化操作
```
from selenium import webdriver
from time import sleep
bro = webdriver.Chrome(executable_path='./chromedriver')

bro.get('https://www.taobao.com/')

#标签定位
search_input = bro.find_element_by_id('q')
#标签交互
search_input.send_keys('Iphone')


#执行一组js程序
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
sleep(2)
#点击搜索按钮
btn = bro.find_element_by_css_selector('.btn-search')
btn.click()


bro.get('https://www.baidu.com')
sleep(2)
#回退
bro.back()
sleep(2)
#前进
bro.forward()


sleep(5)

bro.quit()
```

### 动作链和iframe的处理
```
from selenium import webdriver
from time import sleep
#导入动作链对应的类
from selenium.webdriver import ActionChains
bro = webdriver.Chrome(executable_path='./chromedriver')

bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')

#如果定位的标签是存在于iframe标签之中的则必须通过如下操作在进行标签定位
bro.switch_to.frame('iframeResult')#切换浏览器标签定位的作用域
div = bro.find_element_by_id('draggable')

#动作链
action = ActionChains(bro)
#点击长按指定的标签
action.click_and_hold(div)

for i in range(5):
    #perform()立即执行动作链操作
    #move_by_offset(x,y):x水平方向 y竖直方向
    action.move_by_offset(17,0).perform()
    sleep(0.5)

#释放动作链
action.release()

bro.quit()
```

### 模拟登录qq空间
```
from selenium import webdriver
from time import sleep

bro = webdriver.Chrome(executable_path='./chromedriver')

bro.get('https://qzone.qq.com/')

bro.switch_to.frame('login_frame')

a_tag = bro.find_element_by_id("switcher_plogin")
a_tag.click()


userName_tag = bro.find_element_by_id('u')
password_tag = bro.find_element_by_id('p')
sleep(1)
userName_tag.send_keys('328410948')
sleep(1)
password_tag.send_keys('123456789')
sleep(1)
btn = bro.find_element_by_id('login_button')
btn.click()

sleep(3)

bro.quit()
```

### 谷歌无头浏览器+反检测
```
from selenium import webdriver
from time import sleep
#实现无可视化界面
from selenium.webdriver.chrome.options import Options
#实现规避检测
from selenium.webdriver import ChromeOptions

#实现无可视化界面的操作
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#实现规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

#如何实现让selenium规避被检测到的风险
bro = webdriver.Chrome(executable_path='./chromedriver',chrome_options=chrome_options,options=option)

#无可视化界面（无头浏览器） phantomJs
bro.get('https://www.baidu.com')

print(bro.page_source)
sleep(2)
bro.quit()
```

### 基于selenium实现12306模拟登录
```
#下述代码为超级鹰提供的示例代码
import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

# chaojiying = Chaojiying_Client('bobo328410948', 'bobo328410948', '899370')	#用户中心>>软件ID 生成一个替换 96001
# im = open('12306.jpg', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
# print(chaojiying.PostPic(im, 9004)['pic_str'])
#上述代码为超级鹰提供的示例代码

#使用selenium打开登录页面
from selenium import webdriver
import time
from PIL import Image
from selenium.webdriver import ActionChains
bro = webdriver.Chrome(executable_path='./chromedriver')
bro.get('https://kyfw.12306.cn/otn/login/init')
time.sleep(1)

#save_screenshot就是将当前页面进行截图且保存
bro.save_screenshot('aa.png')

#确定验证码图片对应的左上角和右下角的坐标（裁剪的区域就确定）
code_img_ele = bro.find_element_by_xpath('//*[@id="loginForm"]/div/ul[2]/li[4]/div/div/div[3]/img')
location = code_img_ele.location  # 验证码图片左上角的坐标 x,y
print('location:',location)
size = code_img_ele.size  #验证码标签对应的长和宽
print('size:',size)
#左上角和右下角坐标
rangle = (
int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height']))
#至此验证码图片区域就确定下来了

i = Image.open('./aa.png')
code_img_name = './code.png'
#crop根据指定区域进行图片裁剪
frame = i.crop(rangle)
frame.save(code_img_name)

#将验证码图片提交给超级鹰进行识别
chaojiying = Chaojiying_Client('bobo328410948', 'bobo328410948', '899370')	#用户中心>>软件ID 生成一个替换 96001
im = open('code.png', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
print(chaojiying.PostPic(im, 9004)['pic_str'])
result = chaojiying.PostPic(im, 9004)['pic_str']
all_list = [] #要存储即将被点击的点的坐标  [[x1,y1],[x2,y2]]
if '|' in result:
    list_1 = result.split('|')
    count_1 = len(list_1)
    for i in range(count_1):
        xy_list = []
        x = int(list_1[i].split(',')[0])
        y = int(list_1[i].split(',')[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)
else:
    x = int(result.split(',')[0])
    y = int(result.split(',')[1])
    xy_list = []
    xy_list.append(x)
    xy_list.append(y)
    all_list.append(xy_list)
print(all_list)
#遍历列表，使用动作链对每一个列表元素对应的x,y指定的位置进行点击操作
for l in all_list:
    x = l[0]
    y = l[1]
    ActionChains(bro).move_to_element_with_offset(code_img_ele, x, y).click().perform()
    time.sleep(0.5)

bro.find_element_by_id('username').send_keys('www.zhangbowudi@qq.com')
time.sleep(2)
bro.find_element_by_id('password').send_keys('bobo_15027900535')
time.sleep(2)
bro.find_element_by_id('loginSub').click()
time.sleep(30)
bro.quit()
```

### Flask代码补充
#### test.py
```
from flask import Flask,render_template
import users

app = Flask(__name__)

@app.route('/index')
def index():
    return 'hello'

#注册蓝图
app.register_blueprint(users.user)
if __name__ == '__main__':
    app.run()
```

#### users.py
```
#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Blueprint

#user为蓝图的唯一标识
user = Blueprint('user', __name__)

@user.route('/user',methods=['POST','GET'])
def func():
    return 'this BluePrint of user func'
```
