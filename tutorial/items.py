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

class RADItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()
    facebook = scrapy.Field()
    instagram = scrapy.Field()
    phone = scrapy.Field()
    brand_or_designer = scrapy.Field()
    item_name = scrapy.Field()
    city = scrapy.Field()
    post_code = scrapy.Field()
    street_address = scrapy.Field()
    labeled_size = scrapy.Field()
    rrp = scrapy.Field()
    hire_price = scrapy.Field()
    best_fit_size = scrapy.Field()
    item_views = scrapy.Field()
    date_posted = scrapy.Field()
    description = scrapy.Field()
    
