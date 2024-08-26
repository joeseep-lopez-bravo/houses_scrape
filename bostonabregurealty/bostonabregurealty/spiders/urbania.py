import scrapy


class UrbaniaSpider(scrapy.Spider):
    name = "urbania"
    allowed_domains = ["urbania.pe"]
    start_urls = ["https://urbania.pe/"]

    def parse(self, response):
        pass
