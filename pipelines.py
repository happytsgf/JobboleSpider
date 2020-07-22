# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import  json
import  MySQLdb
import MySQLdb.cursors
from twisted.enterprise import  adbapi
class JobbolespiderPipeline(object):
    def process_item(self, item, spider):
        return item

#写文件pipelines
class JsonWritePipeline(object):
    #1.初始化时用codecs打开文件
    def __init__(self):
        self.file = codecs.open('article.json','w','utf-8')
    def process_item(self, item, spider):
        #1.1.对象转换成字符串
        lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
        #1.2.写入文件
        self.file.write(lines)
        return item
    #2.关闭文件 调用scrapy完成方法
    def spider_closed(self,spider):
        self.file.close()
#调用scrapy export导出类进行导出
class JsonExportPipeline(object):
    #1.初始化导出类 文件名定义  导出对像定义  开始导出
    def __init__(self):
        self.file = open("articleJsonExport.json","wb")
        self.export = JsonItemExporter(self.file,encoding="utf-8", ensure_ascii=False)
        self.export.start_exporting()#开始导出，[ 标识符
    #2.导出操作
    def process_item(self, item, spider):
        self.export.export_item(item)
        return  item
    #3.关闭导出类
    def close_spider(self, spider):
        self.export.finish_exporting() #结束导出，]标识符
        self.file.close()

#创建mysql 驱动pipelines  该类为同步操作，插入数据大时，有可能 堵住
class MysqlPipelines(object):
    #1.定义驱动类,
    def __init__(self):
        #2.创建连接
        self.conn = MySQLdb.connect('127.0.0.1','root','Xtep@2019','python', charset="utf8", use_unicode=True)
        #获取油标
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        #定义sql
        sql = """
            INSERT INTO mook_class (class_name,class_img,class_hard,class_time,class_num,class_score,class_img_path)
            VALUES(%s,%s,%s,%s,%s,%s,%s);
        """
        self.cursor.execute(sql,(item["class_name"],item["class_img"][0],item["class_hard"],item["class_time"],item["class_num"],item["class_score"],item["class_img_path"]))
        self.conn.commit()
        return  item

#使用wtisted 的dbapi进行数据插入
#1.初始化 dbpool连接池
#2.读取setting mysql配置信息
#3.处理item 响应方法process_item(self,item,spider) 进行插入操作
#3.1 item类封装get_insertsql方法
#4.异常事件处理
class MysqlTwistedPipelines(object):
    #初始化
    def __init__(self,dbpool):
        self.dbpool = dbpool
    #读取配置
    @classmethod
    def from_settings(cls,settings):
        dbparam = dict(
            host = settings["MYSQL_HOST"],
           db = settings["MYSQL_DB"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWD"],
            charset='utf8',
            port = settings["MYSQL_PORT"],
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparam)
        return cls(dbpool)

    #3.处理item 响应方法
    def process_item(self,item,spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常
        return item
    def handle_error(self, failure, item, spider):
        print(failure)
    def do_insert(self, cursor, item):
        #根据不同的item 构建不同的sql语句并插入到mysql中
        #if item['class_name']  != "":
            insert_sql, params = item.get_insert_sql()
            cursor.execute(insert_sql, params)


#1.创建自定义图片处理pipelines类
class ArticleImagePipeline(ImagesPipeline):
    #2.重写下载完成方法
    def item_completed(self, results, item, info):
        if "class_img" in item:
            for ok, value in results:
                class_img_path = value["path"]
            item["class_img_path"] = class_img_path
        return item #item修改完后要return回去