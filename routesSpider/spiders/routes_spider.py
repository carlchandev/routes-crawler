import scrapy
import math


class QuotesSpider(scrapy.Spider):
    name = "routes"
    start_urls = [
        'http://www.walkonhill.com/route.php?area=1&seq=1',
        # http://www.walkonhill.com/route_en.php?area=1&seq=1 // following link?
    ]

    def parse(self, response):
        generalInfo = response.css(
            'div.generalInfo td.right_td::text').getall()
        yield {
            'name': generalInfo[0],
            'description': response.css('p.intro::text').get(),
            'distanceInKm': generalInfo[1].replace(' 公里', '').replace('.0', ''),
            'durationInHour': generalInfo[2].replace(' 小時', ''),
            'difficulty': math.ceil(float(response.css('p.current_rating::text').get()))
        }
