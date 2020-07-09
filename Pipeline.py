# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,logging
from scrapy.exceptions import DropItem

from .items import QuanshuItem,QuanshuItemchapter
login=logging.getLogger(__name__)

class QuanshuPipeline(object):
    def open_spider(self, spider):
        data_config = spider.settings["DATBASE_CONFIG"]
        if data_config["type"] == "mysql":
            self.conn = pymysql.connect(**data_config["config"])
            self.cursor = self.conn.cursor()  # 创建游标
            spider.conn = self.conn
            spider.cursor = self.cursor

    def process_item(self, item, spider):
        if isinstance(item, QuanshuItem):
            sql = "select id from novel where  book_name=%s and author=%s"
            self.cursor.execute(sql, (item["book_name"], item["author"]))
            #写入小说信息
            if not self.cursor.fetchone():
                try:
                    sql = "insert into novel(category,author,book_name,status,description,c_time,url)" \
                    "values(%s,%s,%s,%s,%s,%s,%s)"
                    self.cursor.execute(sql,(
                        item["category"],
                        item["author"],
                        item["book_name"],
                        item["status"],
                        item["description"],
                        item["c_time"],
                        item["url"]

                    ))
                    self.conn.commit()#提交数据
                except Exception as e:#捕获异常
                    self.conn.rollback()
                    login.warning("小说信息有问题 url=%s %s"%(item["url"],e))

            # 写入章节信息 
                try:
                    sql="insert into chapter (novel_id,title, order_num,c_time,url)"\
                        "values (%s,%s,%s,%s,%s)"
                # 获取章节信息的数据
                    novel_id=self.cursor.lastrowid#取最后一行，即最新的数据消息
                    data_list=[]
                except Exception as e:
                    self.conn.rollback()
                    login.warning("小说章节有问题 url=%s %s" % (item["url"], e))


            #取title

            for index,chapter in enumerate(item["chapter_list"]):
                title,url=chapter       #元组赋值
                order_num=index
                c_time=item["c_time"]
                data_list.append((novel_id,title,order_num,c_time,url))
            #数据库chapter表中数据已经拿完可以进行插入数据
            self.cursor.executemany(sql,data_list)
            self.conn.commit() #数据提交到数据库
            return  item

        elif isinstance(item,QuanshuItemchapter):
            sql="update chapter set content=%s where id=%s"
            self.cursor.execute(sql,(item["content"],item["chapter_id"]))
            self.conn.commit()
            return item
        else:
            return DropItem


    def close_spider(self,spider):
        data_config = spider.settings["DATBASE_CONFIG"]
        if data_config["type"] == "mysql":
            self.conn = pymysql.connect(**data_config["config"])
            spider.conn.close()
            spider.cursor.close()

