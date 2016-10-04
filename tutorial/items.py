# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class DmozItem(scrapy.Item):
  title = scrapy.Field()
  link = scrapy.Field()
  desc = scrapy.Field()

class StarNowItem(scrapy.Item):
    name = scrapy.Field()
    height = scrapy.Field()
    waist = scrapy.Field()
    chest = scrapy.Field()
    hips = scrapy.Field()
    weight = scrapy.Field()
