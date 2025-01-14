import scrapy


class OlympicsSpider(scrapy.Spider):
    name = "olympics"
    allowed_domains = ["www.olympedia.org"]
    start_urls = ["https://www.olympedia.org/results/19000014"]

    def parse(self, response):
        pass
