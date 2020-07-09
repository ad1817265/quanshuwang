# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuanshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    book_name = scrapy.Field()
    status= scrapy.Field()
    description = scrapy.Field()
    c_time = scrapy.Field()
    url = scrapy.Field()
    chapter_list = scrapy.Field()
class QuanshuItemchapter(scrapy.Item):
    content = scrapy.Field()
    url = scrapy.Field()
    chapter_id = scrapy.Field()


