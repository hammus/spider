import scrapy
import logging
import re
import urllib
from scrapy.utils.log import configure_logging

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

h = HTMLParser()

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

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
    rad_url = scrapy.Field()



class RADSpider(scrapy.Spider):

    name = "rad"
    allowed_domains = ["rentadressaustralia.com"]
    start_urls = [
        "http://rentadressaustralia.com/browse/Dresses/?page=1"
        ]

    def parse(self, response):
        for href in response.xpath("//div[@class='thumbnail']/div[@class='caption']/h1/a/@href").extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_details)

        s = h.unescape(response.xpath("//a[@class='nextPageSelector']/@href").extract_first())
        next_page = "".join(s.split())
        print(next_page)
        # print next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def parse_details(self, response):
        def extract_xpath(nodes, query):
            return response.xpath(query).extract()


        # catNodes = response.xpath("//table[@id = 'ctl00_cphMain_physicalDetails_memberAttributes']//td")
# //*[@id="summary"]/div/div/div[1]/dl/dd[6]/text() //*[@id="summary"]/div/div/div[1]/dl/dd[9]/span
        item = RADItem()
        item["name"] = ' '.join(extract_xpath(response, "/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/ul/li[1]/h4/text()")).strip()
        try:
            scriptText = ' '.join(extract_xpath(response, "/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/ul/li[4]/span/script/text()")).strip()
            emailHex = re.search('^eval\(unescape\(\'(.*)\'\)\)$', scriptText).group(1)
            email = re.search("^document.write\(\'\<a\shref\=\"mailto:(.*)\"\s\>Send E-mail</a>'\);", urllib.unquote(emailHex)).group(1)
            item["email"] = email
        except AttributeError: 
            print("No Email Detected")
            item["email"] = ""
        item["phone"] = ' '.join(extract_xpath(response, "/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/ul/li[3]/text()")).strip()
        item["facebook"] = ' '.join(extract_xpath(response, "/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a[1]/@href")).strip()
        item["instagram"] = ' '.join(extract_xpath(response, "/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a[2]/@href")).strip()
        item["item_name"] = ' '.join(extract_xpath(response, "/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a[2]/@href")).strip()
        item["brand_or_designer"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[1]/text()[1]")).strip()
        item["city"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[3]/text()[1]")).strip()
        item["rad_url"] = response.url
        item["post_code"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[5]/text()[1]")).strip()
        item["street_address"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[6]/text()")).strip()
        item["labeled_size"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[7]/text()[1]")).strip()
        item["rrp"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[8]/span/text()")).strip()
        item["hire_price"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[9]/span/text()")).strip()
        item["best_fit_size"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[11]/text()[1]")).strip()
        item["item_views"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[13]/text()")).strip()
        item["date_posted"] = ' '.join(extract_xpath(response, "//*[@id='summary']/div/div/div[1]/dl/dd[14]/text()")).strip()
        item["description"] = ' '.join(extract_xpath(response, "//*[@id='Description']/div/div/p[1]/text()")).strip()

        yield item
