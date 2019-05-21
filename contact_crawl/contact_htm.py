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


source_file = "nan.csv"
result_file = "nan_contact.csv"


company_list = []

lines = linecache.getlines(source_file)
for line in lines:
    data = line[1:].strip().split(',')
    company_list.append(data[1])
linecache.clearcache()

company_list = list(set(company_list))
print("总共需要爬去{0}个商家信息".format(len(company_list)))

contact_list = [(raw_url, raw_url + '/page/contactinfo.htm') for raw_url in company_list]

# company_list = [
#     "https://huajunzhiyi.1688.com",
#     "https://shop1482206425147.1688.com",
#     "https://shop9103636635809.1688.com",
#     "https://shop1472566760481.1688.com",
#     "https://shop1457542848269.1688.com",
# ]

driver = webdriver.Firefox()
# chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# driver = webdriver.Chrome(chromedriver)

# 淘宝登录的url
login_url = 'https://login.taobao.com/member/login.jhtml'
# 跳转到登录页面
driver.get(login_url)
time.sleep(20)


# 构建agents防止反爬虫
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1;.NET CLR 1.1.4322; .NET CLR2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5(like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
]

f = open(result_file, 'w')


count = 0
for (company_url, contact_url) in contact_list:
    try:
        driver.get(contact_url)

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


        # pattern = re.compile(r'<dt>电.*话：</dt>\n +<dd>[\d ]+</dd>', re.S)
        # pattern = re.compile('<div class="contcat-desc".*?>(.*?)</div>', re.S)
        tel_pattern = re.compile('<dt>电.*话：</dt>\n +<dd>([\d ]+)</dd>', re.S)
        response = driver.page_source
        # info = re.findall(pattern, response)
        telecom = ""
        telecom_num = re.findall(tel_pattern, response)
        if telecom_num:
            telecom = telecom_num[0].strip().replace(" ", "-")
        info_list.append(telecom)

        line = ','.join(info_list) + '\n'

        f.write(line)
        print(line,)

    except Exception as e:
        print(contact_url)
        print(repr(e))
    time.sleep(5)

    count += 1

    if count % 50 == 0:
        print("已爬去{0}个商家，共需要爬去{1}个商家。".format(count, len(contact_list)))

# 关闭csv
f.close()
# 关闭模拟浏览器
driver.close()