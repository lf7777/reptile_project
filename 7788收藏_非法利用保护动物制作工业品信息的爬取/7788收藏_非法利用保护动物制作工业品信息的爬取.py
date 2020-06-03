from selenium import webdriver
import time
import requests
from lxml import etree

# 创建浏览器对象，相比于普通的爬虫程序，这里我使用了selenium模块,它可以找到网页的搜索框，并能输入内容，然后再通过爬虫模块获取html的信息
d = webdriver.Chrome()

# 通过刚才创建的浏览器对象，进行目标网页的访问
d.get('http://997788.com')

time.sleep(3)

# 通过 css id找到搜索栏，并输入内容自定义的内容 
d.find_element_by_id('s0').send_keys('xiang牙')

time.sleep(1)
# 点击搜索按钮
d.find_elements_by_name('submit')[0].click()

# 获取搜索之后的url,供爬虫程序使用
url = d.current_url

# 设置请求头，将自己伪装成一个正常的浏览器，达到避开目标服务器的反爬策略
headers = {
    'Referer':'https://www.997788.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

# 获取html的信息
rep = requests.get(url,headers=headers,verify=False)

# with open('xiang牙.html','rb') as fr:
#     data = fr.read().decode('utf-8')

# tree = etree.HTML(data)

# 实例化一个xpath的html对象,该模块对爬取下来的信息进行定位
tree = etree.HTML(rep.text)

table = tree.xpath('//table[@class="tbc"]')

for i in range(0,len(table)-1):
    #店家名称
    business = table[i].xpath('./tr/td[1]/a/font/text()')[0]
    #店家所在地
    place = table[i].xpath('./tr/td[1]/font[1]/text()')[0]
    # xinyu = table[i].xpath('./tr/td[1]/a[2]/font/text()')
    #商品名称
    name = table[i].xpath('./tr/td[2]//a')[0].attrib.get('title').split('-')[0]
    #商品价格
    price = table[i].xpath('./tr/td[5]/font[1]//text()')
    if '\n' in price[0]:
        price.pop(0)

    # 匹配excel格式，保存excel的信息到本地
    with open("c:/Users/Administrator/Documents/Result",'a')as fa:
        fa.write(business+' '+place+' '+name+' '+price[0]+'\n')