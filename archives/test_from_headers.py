import scrapy


class HeadersSpider(scrapy.Spider):
    name = "test_from_headers"
    playwright = 1

    def start_requests(self):
        yield scrapy.Request(
            url="https://apuestas.retabet.es/deportes/baloncesto/nba-s41",
            meta={"playwright": int(self.playwright)},
        )

    def parse(self, response):
        print(response.url)
        print(response.text)
        yield {"url": response.url}
