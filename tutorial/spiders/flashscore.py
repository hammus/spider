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

class NRLTeam(scrapy.Item):
    name = scrapy.Field()
    icon = scrapy.Field()
    image_urls = scrapy.Field()


class FlashSpider(scrapy.Spider):

    name = "flashscore"
    root_domain = "https://www.flashscore.com.au"
    allowed_domains = ["flashscore.com.au"]
    start_urls = [
        "https://www.flashscore.com.au/league/australia/nrl/teams/"
        ]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.xpath("//div[@id='tournament-page-participants']/table/tbody/tr/td/a/@href").extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_details)
        
    def parse_details(self, response):
        def extract_xpath(nodes, query):
            return response.xpath(query).extract()

        item = NRLTeam()
        print("--------------------------- NRL RESULTS ---------------------------")
        # .fs-table.tournament-page-participants td a
        # tournamentIconStyleAttr = response.xpath("//div[@class='tournament-logo']/@style").extract_first()
        # tournamentIconUriSuffix = re.search('^background\-image\:\surl\((.*)\)', tournamentIconStyleAttr).group(1)
        # tournamentIconUri = f"{self.root_domain}/{tournamentIconUriSuffix}"
        # self.image_urls.append(tournamentIconUri)

        teamIconBGStyle = response.xpath("//div[@class='team-logo']/@style").extract_first()
        teamIconUriSuffix = re.search('^background\-image\:\surl\((.*)\)', teamIconBGStyle).group(1)
        iconUrl = f"{self.root_domain}/{teamIconUriSuffix}"
        item["image_urls"][0] = iconUrl
        item["icon"] = iconUrl
        item["name"] = response.xpath("//div[@class='team-name']/text()").extract()[0]

        
        print("--------------------------- END NRL RESULTS ---------------------------")

        yield item    
