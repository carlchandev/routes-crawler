import scrapy


class QuotesSpider(scrapy.Spider):
    name = "routes"
    start_urls = [
        'http://www.walkonhill.com/route.php?area=1&seq=1',
        # http://www.walkonhill.com/route_en.php?area=1&seq=1 // following link?
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'name': quote.css('span.text::text').get(),
            }
