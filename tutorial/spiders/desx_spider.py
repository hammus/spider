import scrapy
import logging
from scrapy_splash import SplashRequest
from scrapy.utils.log import configure_logging
from scrapy.selector import Selector

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

h = HTMLParser()

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

class DSXItem(scrapy.Item):
    dress_brand = scrapy.Field()
    dress_name = scrapy.Field()
    rental_price = scrapy.Field()
    rrp = scrapy.Field()
    size = scrapy.Field()
    rental_period_days = scrapy.Field()
    profile_url = scrapy.Field()
    location_suburb = scrapy.Field()
    location_state = scrapy.Field()
    shipping_details = scrapy.Field()
    labeled_size = scrapy.Field()
    url = scrapy.Field()

base_url = "https://designerex.com.au"



class DSXSpider(scrapy.Spider):

    name = "dsx"
    allowed_domains = ["designerex.com.au"]

    start_urls = [
        "https://designerex.com.au/search?utf8=%E2%9C%93&designer_brand=&size=&target_date=&target_date_selector="
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})



    def parse(self, response):
        for item_url in response.css('div.item > a').xpath('@href').extract():
            yield SplashRequest(base_url + item_url, self.parse_item, args={'wait': 0.5})

        a_next = response.css('a[rel="next"]').xpath('@href').extract_first()
        if a_next is not None:
            next_page = response.urljoin(a_next)
            yield SplashRequest(next_page, self.parse, args={'wait': 0.5})

    def parse_item(self, response):
        item = DSXItem()
        item["dress_brand"] = response.css('h3#dress_brand::text').extract()
        item["dress_name"] = response.css('div.dress_name::text').extract_first()
        item["rental_price"] = response.css('span#rental_price_::text').extract()
        item["rrp"] = response.css('div.rrp::text').extract_first().split("$")[1]
        _size = response.css('input#reservation_size').xpath('@value').extract_first()
        if _size is not None and _size.isdigit():
            item["size"] = int(_size)
        else:
            item["size"] = "Not Listed"
        item["profile_url"] = response.css('a#profile_image').xpath('@href').extract()
        item["location_suburb"] = response.css('span.dress_user_area.user_area > div::text').extract_first()
        item["location_state"] = response.css('span.dress_user_area.user_area > div > span.spacer5left::text').extract_first()
        item["rental_period_days"] = response.css('input#reservation_rental_period').xpath('@value').extract_first()
        item["url"] = response.url
        yield item
