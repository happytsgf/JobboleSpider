# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


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





