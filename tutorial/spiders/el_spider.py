import scrapy

from scrapy.utils.log import configure_logging


class ELItem(scrapy.Item):
    name = scrapy.Field()
    height = scrapy.Field()
    waist = scrapy.Field()
    chest = scrapy.Field()
    hips = scrapy.Field()

class ELSpider(scrapy.Spider):
    name = "el"
    allowed_domains = ["elpromotions.co.uk"]
    start_urls = [
        "http://elpromotions.co.uk/category/uk/female/"
        ]

    def parse(self, response):
        for href in response.xpath("//div[@class='model']/div[@class='model_image']/a/@href").extract():
            yield scrapy.Request(href, callback=self.parse_details)

        next_page = response.xpath("//div[@class='paged']/div[@class='alignright']/a[contains(text(),'More')]/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def parse_details(self, response):
        def extract_xpath(nodes, query):
            return response.xpath(query).extract()


        item = ELItem()
        item["name"] =  response.xpath("//div[@class = 'port_right']/h2/text()").extract_first()
        item["height"] = response.xpath("//div[@class = 'name' and text()='Height:']/following-sibling::div/a/text()").extract_first()
        item["waist"] = response.xpath("//div[@class = 'name' and text()='Waist:']/following-sibling::div/a/text()").extract_first()
        item["hips"] = response.xpath("//div[@class = 'name' and text()='Hips:']/following-sibling::div/a/text()").extract_first()
        item["chest"] = response.xpath("//div[@class = 'name' and text()='Chest:']/following-sibling::div/a/text()").extract_first()
        yield item
