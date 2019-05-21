# 1688-shop-crawl

通过selenium、scrapy爬去阿里巴巴的商户信息  
输入是同学已经爬好的商户数据 nan.csv  
该数据是通过1688搜索界面的异步加载接口得到的  

contact_crawl: 
>使用selenium爬去1688商户的联系方式等信息
>运行方式，直接运行contact_html.py文件即可

info_scrapy: 
>使用scrapy框架爬去1688手机端接口的商户信息
>运行方式，scrapy框架下直接运行1688-shop-crawl/m_info_scrapy/scrapy_1688/spiders/m_company.py