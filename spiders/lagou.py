# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from JobboleSpider.items import LagouJobItemLoader,LagouJobItem



class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com//']

    """
       1.定义crawlespider 命令：scrapy genspider -t crawl lagou www.lagou.com/
       1.1设置url规则【支持正则表达式规则】 过滤我们需要爬取的Url(不用设置callback),以爬取内容的url（设置callback）
       2。重写parse方法，进行处理数据 
       3。使用scrapyItemLoader进行解析 respones数据
       
    """


    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        Rule(LinkExtractor(allow="gongsi/j\d+.html"),  follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
        # Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        # Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        # Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_job(self, response):
        print("entry the parse_job")
        item_loader = LagouJobItemLoader(item=LagouJobItem, response=response)
        item_loader['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()

        return item_loader.load_item()
