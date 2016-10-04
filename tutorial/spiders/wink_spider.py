import scrapy


class WinkItem(scrapy.Item):
    name = scrapy.Field()
    height = scrapy.Field()
    waist = scrapy.Field()
    chest = scrapy.Field()
    hips = scrapy.Field()

class WinkSpider(scrapy.Spider):
    name = "wink"
    allowed_domains = ["winkmodels.com.au"]
    start_urls = [
        "http://winkmodels.com.au/models/vic/female/models/"
        ]

    def parse(self, response):
        with open('wink.html', 'wb') as f:
            f.write(response.body)

    #     for model in response.xpath("//div[@class='ais-hits--item']"):
    #         yield self.parse_details(model)
    #
    #     next_page = response.xpath("//div[@class='paged']/div[@class='alignright']/a[contains(text(),'More')]/@href").extract_first()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse)
    #
    #
    #
    # def parse_details(self, response):
    #     def extract_xpath(nodes, query):
    #         return response.xpath(query).extract()
    #
    #
    #     item = WinkItem()
    #     item["name"] =  response.xpath("//div[@class = 'port_right']/h2/text()").extract_first()
    #     item["height"] = response.xpath("//div[@class = 'name' and text()='Height:']/following-sibling::div/a/text()").extract_first()
    #     item["waist"] = response.xpath("//div[@class = 'name' and text()='Waist:']/following-sibling::div/a/text()").extract_first()
    #     item["hips"] = response.xpath("//div[@class = 'name' and text()='Hips:']/following-sibling::div/a/text()").extract_first()
    #     item["chest"] = response.xpath("//div[@class = 'name' and text()='Chest:']/following-sibling::div/a/text()").extract_first()
    #     yield item
