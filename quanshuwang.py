# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy_redis.spiders import RedisSpider

from ..items import QuanshuItem,QuanshuItemchapter
# class QuanshuwangSpider(scrapy.spider):#scrapy时换成scrapy。spider
class QuanshuwangSpider(RedisSpider):#scrapy时换成scrapy。spider
    name = 'quanshuwang'
    # allowed_domains = ['dd']
    start_urls = ['http://www.quanshuwang.com/list/2_1.html']
    # 起始请求放在公共区域

    def parse(self, response):
        novel_urls=response.xpath('//ul[@class="seeWell cf"]/li/a/@href').extract()
        for novel_url in novel_urls[:1]:
            yield scrapy.Request(novel_url,callback=self.get_novel_massage)

    def get_novel_massage(self,response):
        item=QuanshuItem()
        category=response.xpath('//meta[@property="og:novel:category"]/@content').extract_first()
        author=response.xpath('//meta[@property="og:novel:author"]/@content').extract_first()
        book_name=response.xpath('//meta[@property="og:novel:book_name"]/@content').extract_first()
        status=response.xpath('//meta[@property="og:novel:status"]/@content').extract_first()
        des = response.xpath('//meta[@property="og:description"]/@content').extract_first()
        des.split("<br />")
        description="".join([i.strip() for i in des])
        c_time=datetime.datetime.now()
        url=response.url
        item["category"]=category
        item["author"]=author
        item["book_name"]=book_name
        item["status"]=status
        item["c_time"]=c_time
        item["description"]=description
        item["url"]=url
        chapyter_url=response.xpath('//div[@class="b-oper"]/a[@class="reader"]/@href').extract_first()
        yield scrapy.Request(url=chapyter_url,callback=self.get_info,meta={"novel":item})



    def get_info(self,response):
        novel_item=response.meta["novel"]
        chapter_list=[]
        list=response.xpath('//div[@class="clearfix dirconone"]/li/a')
        for li in list:
            chapter=li.xpath('./@href').extract()[0]
            title=li.xpath('./text()').extract()[0]
            a=chapter_list.append((title,chapter))
        novel_item["chapter_list"]=chapter_list
        yield novel_item
        sql="select id,url from chapter where content is null"
        self.cursor.execute(sql)
        for item in self.cursor.fetchall():
            yield scrapy.Request(url=item[1],callback=self.get_content,meta={"id":item[0]})


    def get_content(self,response):
        item=QuanshuItemchapter()
        chapter_id=response.meta["id"]
        contents= response.xpath('//div[@class="mainContenr"]/text()').extract()
        content=" ".join([i.strip() for i in contents])
        item["content"]=content
        item["chapter_id"]=chapter_id
        item["url"]=response.url
        yield item


