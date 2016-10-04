import scrapy
import logging

from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.CRITICAL
)

class StarNowItem(scrapy.Item):
    name = scrapy.Field()
    height = scrapy.Field()
    waist = scrapy.Field()
    chest = scrapy.Field()
    hips = scrapy.Field()
    weight = scrapy.Field()
    url = scrapy.Field()




class StarNowSpider(scrapy.Spider):
    name = "starnow"
    allowed_domains = ["starnow.com.au"]
    start_urls = [
        "http://www.starnow.com.au/talent/australia/new-south-wales/?gender=f"
        ]

    def parse(self, response):
        for href in response.css('a.headshot::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_details)

        next_page = response.xpath("//div[@class='paging']/a[text()='>>']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def parse_details(self, response):
        def extract_xpath(nodes, query):
            return response.xpath(query).extract()


        catNodes = response.xpath("//table[@id = 'ctl00_cphMain_physicalDetails_memberAttributes']//td")


        item = StarNowItem()
        item["name"] = ' '.join(extract_xpath(response, "//h1[@class = 'profile__name']/text()")).strip()
        item["height"] = ' '.join(catNodes.xpath("div[@class='th' and text()='Height:']/parent::td/text()").extract()).strip().split("/")[0]
        item["waist"] = ' '.join(catNodes.xpath("div[@class='th' and text()='Waist:']/parent::td/text()").extract()).strip().split("/")[0]
        item["hips"] = ' '.join(catNodes.xpath("div[@class='th' and text()='Hips:']/parent::td/text()").extract()).strip().split("/")[0]
        item["chest"] = ' '.join(catNodes.xpath("div[@class='th' and text()='Chest:']/parent::td/text()").extract()).strip().split("/")[0]
        item["weight"] = ' '.join(catNodes.xpath("div[@class='th' and text()='Weight:']/parent::td/text()").extract()).strip().split("/")[0]
        item["url"] = response.url
        yield item
