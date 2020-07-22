# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import  Request
from JobboleSpider.items import JobbolespiderItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['www.imooc.com']
    start_urls = ['https://www.imooc.com/course/list?page=29']

    def parse(self, response):
        """
        1.提取出文章列表所有的url ,交给scrapy进行下载前解析
        2.获取下一页的url交给scrapy进行下载 ，下载完成后交给parse处理
        :param response:
        :return:
        """
        #post_urls = response.xpath('//*[@class="course-card-container"]/a[@class="course-card"]/@href')
        post_urls = response.xpath('//*[@class="course-card-container"]/a[@class="course-card"]')
        for post_node in post_urls:
            post_url = post_node.xpath('./@href').extract_first("")
            img_url = post_node.xpath('./div/img[@class="course-banner lazy"]/@data-original').extract_first("")

            #组合url：主域名+具体课程url
            url = parse.urljoin(response.url,post_url)
            #parse.urljoin(response.url, post_url)
            print("课程完整url:"+url)

            #初始化reuqest 方法，交给scrapy进行下载 详情页
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":parse.urljoin(response.url,img_url)},callback=self.pase_detail)
            #yield Request(url='https://www.imooc.com/learn/1199',callback=self.pase_detail)

        #2.获取下一页的url交给scrapy进行下载 ，下载完成后交给parse处理

        next_urls = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/a')#.extract_first("")
        for next_url in  next_urls:
            #print("开始for循环拿下一页:")
            a_name = next_url.xpath('./text()').extract_first("")
            if a_name == "下一页":
                url = next_url.xpath('./@href').extract_first("")
                print("下一页url:"+parse.urljoin(response.url,url))
                #提取下一页并交给scrapy进行下载
                # yield Request(url=parse.urljoin(response.url,url),callback=self.parse)
                #print("跳出for循环:")
                break

        #re_selector1 = response.xpath('/html/body/div[4]/div[3]/div/h3/span')
        #re_selector = response.xpath('//*[@id="main"]/div[2]/div[2]/div[1]/div/div[1]/a/div[2]/h3/text()')


        #with open('baidu.html', 'w', encoding='utf-8') as f:
        #    f.write(response.body.decode('utf-8'))
        pass
    def pase_detail(self,response):
        #定义item类
        job_item = JobbolespiderItem()

        class_name = response.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/h2/text()').extract_first("")
        job_item["class_name"] = class_name
        job_item["class_img"] = [response.meta.get("front_image_url","")]
        print("课程名称："+class_name)
        print("图片url:"+response.meta.get("front_image_url",""))
        class_infos = response.css('.static-item')
        for i  in range(len( class_infos)):
            class_info = class_infos[i]
            title = class_info.css(".meta::text").extract_first("")
            #value = class_info.css(".meta-value ::text").extract_first("")
            value = class_info.xpath("./span[2]/text()").extract_first("")
            if i==0:
                class_hard = value
                job_item["class_hard"] = class_hard
                print("第 "+str(i)+" 个 class_hard  信息："+title +"  "+class_hard)
            elif i==1:
                class_time = value
                job_item["class_time"] = class_time
                print("第 "+str(i)+" 个 class_time  信息："+title +"  "+class_time)
            elif i==2:
                class_num = value
                job_item["class_num"] = class_num
                print("第 "+str(i)+" 个 class_num  信息："+title +"  "+class_num)
            else:
                class_score = value
                job_item["class_score"] = class_score
                print("第 "+str(i)+" 个 class_score  信息："+title +"  "+class_score)
        yield  job_item #触发scrapy调用pipelines方法
        pass