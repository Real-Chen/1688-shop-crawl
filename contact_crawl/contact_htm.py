from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import urllib
# import urllib2
import sys
import os
import re
import csv
import numpy as np
import random
import linecache

# 导入需要爬去的网页
source_file = "tong.csv"

company_list = []
lines = linecache.getlines(source_file)
for line in lines:
    data = line[1:].strip().split(',')
    company_list.append(data[1])
linecache.clearcache()

company_list = list(set(company_list))
print("总共需要爬去{0}个商家信息".format(len(company_list)))

contact_list = [(raw_url, raw_url + '/page/contactinfo.htm') for raw_url in company_list]


# 开启selenium浏览器
driver = webdriver.Firefox()

# 淘宝登录的url
login_url = 'https://login.taobao.com/member/login.jhtml'
# 跳转到登录页面
driver.get(login_url)
# 等待20s手动扫码登陆
time.sleep(20)

# 开始爬虫
count = 0
for (company_url, contact_url) in contact_list:
    try:
        driver.get(contact_url)

        # 使用xpath解析数据
        title = driver.find_elements_by_xpath('''//div[@class="contact-info"]/h4''')
        people = driver.find_elements_by_class_name("membername")
        mobile_num = driver.find_elements_by_xpath('''//dl[@class="m-mobilephone"]/dd''')
        area = driver.find_elements_by_xpath('''//div[@class="item address fd-clr"]//span''')
        address = driver.find_elements_by_xpath('''//dd[@class="address"]''')

        raw_info_list = [title, people, mobile_num, area, address]

        info_list = [company_url]
        for infos in raw_info_list:
            if infos:
                info_list.append(infos[0].text)
            else:
                info_list.append('')

        # 使用正则表达式解析电话
        tel_pattern = re.compile('<dt>电.*话：</dt>\n +<dd>([\d ]+)</dd>', re.S)
        response = driver.page_source
        telecom = ""
        telecom_num = re.findall(tel_pattern, response)
        if telecom_num:
            telecom = telecom_num[0].strip().replace(" ", "-")
        info_list.append(telecom)

        line = ','.join(info_list) + '\n'
        print(line,)

    except Exception as e:
        print(contact_url)
        print(repr(e))
    time.sleep(5)

    count += 1

    if count % 50 == 0:
        print("已爬去{0}个商家，共需要爬去{1}个商家。".format(count, len(contact_list)))

# 关闭模拟浏览器
driver.close()