#!/usr/bin/python
# -*- coding: UTF-8 -*

import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from scrapy import cmdline
import re
import linecache
import pandas as pd

class mInfoSpider(scrapy.Spider):
    name = "m_detail_info"
    allowed_domains = ["1688.com"]

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
    }

    def start_requests(self):
        lines = linecache.getlines('tong.csv')
        start_urls = []
        for line in lines[1:]:
            data = line.strip().split(',')
            company_url = data[1]
            member_id = data[2]
            m_url = "https://m.1688.com/winport/company/%s.html" % (member_id)
            start_urls.append((company_url, m_url))
        linecache.clearcache()
        print("总共有{}条信息。".format(len(start_urls)))
        # f = open('result/tong_m.csv')
        for (root_url, url) in start_urls:
            yield Request(
                url,
                headers=self.headers,
                callback=self.parse
            )

    def parse(self, response):
        result_file = "tong_m.csv"

        # 解析xpath数据
        tags = response.xpath('//div[@class="info-tag-list"]/a/text()')
        chengxintong = response.xpath('//div[@class="auto-summary-div tp-logo"]/*/text()')
        peoples = response.xpath('//*[@id="scroller"]/div[4]/ul/li[1]/div/span/text()')
        check = response.xpath('//div[@class="archive-authinfo-summary"]/ul/li[2]//text()')

        # 清洗数据
        tag_str = '|'.join([tag.extract().strip() for tag in tags]).encode('utf8')
        chengxintong_str = ''.join([data.extract().strip() for data in chengxintong]).encode('utf8')
        people_str = '|'.join([data.extract().strip() for data in peoples]).encode('utf8').replace('\n', '').replace(',', '').replace(' ', '')
        check_str = ''.join([data.extract().strip() for data in check]).encode('utf8')

        url_str = response.url
        member_id = url_str.split('/')[-1].replace(".html", "")
        str_l = [tag_str, chengxintong_str, people_str, check_str]
        print(','.join(str_l))

        dataframe = pd.DataFrame(
            {'member_id': [member_id], 'chengxintong': [chengxintong_str], 'check_info': [check_str], 'tags': [tag_str], 'infos': [people_str]})
        # dataframe = pd.DataFrame([member_id, tag_str, chengxintong_str, people_str, check_str])
        dataframe.to_csv(result_file, mode='a', index=False,header=False,sep=',')

if __name__ == '__main__':
    # cmdline.execute("scrapy crawl company".split())
    cmdline.execute("scrapy crawl m_detail_info".split())