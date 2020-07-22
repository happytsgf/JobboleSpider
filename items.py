# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags
from JobboleSpider.settings import SQL_DATETIME_FORMAT

class JobbolespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    class_name = scrapy.Field()
    class_hard = scrapy.Field()
    class_time = scrapy.Field()
    class_num = scrapy.Field()
    class_score = scrapy.Field()
    class_img = scrapy.Field()#图片url
    class_img_path = scrapy.Field()#图片存放路径

    def get_insert_sql(self):
        sql = """
            INSERT INTO mook_class (class_name,class_img,class_hard,class_time,class_num,class_score,class_img_path)
            VALUES(%s,%s,%s,%s,%s,%s,%s);
        """
        param = [self.class_name,self.class_img,self.class_hard,self.class_time,self.class_num,self.class_score,self.class_img_path]
        return sql,param

def remove_splash(value):
    #去掉工作城市的斜线
    return value.replace("/","")

def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)



class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class LagouJobItem(scrapy.Item):

    #拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor = Join(",")
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):

        insert_sql = """
            insert into lagou_job(title, url, url_object_id, salary, job_city, work_years, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url,
            tags, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"],
            self["work_years"], self["degree_need"], self["job_type"],
            self["publish_time"], self["job_advantage"], self["job_desc"],
            self["job_addr"], self["company_name"], self["company_url"],
            self["job_addr"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params






