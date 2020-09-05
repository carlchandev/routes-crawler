import scrapy
import math
import urllib.parse as urlparse
from urllib.parse import parse_qs
from mergedeep import merge


class QuotesSpider(scrapy.Spider):
    name = "routes"
    start_urls = [
        'http://www.walkonhill.com/route.php?area=1&seq=1',
        # 'http://www.walkonhill.com/route.php?area=1&seq=2',
        # http://www.walkonhill.com/route_en.php?area=1&seq=1 // following link?
    ]
# TODO: DUPEFILTER_CLASS, aviod hitting server too quickly

    def parse(self, response):
        areaToRegion = {
            '0': '香港島',
            '1': '香港島',
            '2': '九龍',
            '3': '新界',
            '4': '香港島',
            '5': '香港島',
            '6': '香港島',
            '7': '離島',
            '8': '離島'
        }
        url = response.url
        queryString = parse_qs(urlparse.urlparse(url).query)
        area = queryString['area'][0]
        paths = response.css('div#trackpointList ol li a::text').getall()
        generalInfo = response.css(
            'div.generalInfo td.right_td::text').getall()
        trail = {
            'name': generalInfo[0],
            'name_en': 'XXX',
            'description': response.css('p.intro::text').get(),
            'description_en': 'XXX',
            'regions': [{
                'name': areaToRegion[area],
                'name_en': 'XXX TODO'
            }],
            'districts': [{
                'name': response.css('p#indicator::text').get().split('\\')[2].strip(),
                'name_en': 'XXX TODO'
            }],
            'height': 9999,  # TODO
            'distanceInKm': generalInfo[1].replace(' 公里', '').replace('.0', ''),
            'difficulty': math.ceil(float(response.css('p.current_rating::text').getall()[0])),
            'durationInHour': generalInfo[2].replace(' 小時', ''),
            'sceneRating': math.ceil(float(response.css('p.current_rating::text').getall()[1])),
            'recommendRating': 3,
            'route': {
                'starts': [
                    {
                        'name': 'TODO',
                        'name_en': 'TODO',
                        'description': response.css('div#tab-1 p::text')[0].get().strip(),
                        'description_en': 'TODO',
                        'marker': {
                            'latitude': 22.281084,
                            'longitude': 114.160931
                        }
                    }
                ],
                'paths': [
                    {
                        'name': 'TODO',
                        'name_en': 'TODO',
                        'description': location.strip(),
                        'description_en': 'TODO',
                        'marker': {
                            'latitude': 22.281084,
                            'longitude': 114.160931
                        }
                    } for location in paths
                ],
                'ends': [
                    {
                        'name': 'TODO',
                        'name_en': 'TODO',
                        'description': response.css('div#tab-1 p::text')[1].get().strip(),
                        'description_en': 'TODO',
                        'marker': {
                            'latitude': 22.281084,
                            'longitude': 114.160931
                        }
                    }
                ]
            },
            "images": [
                {
                    "url": "TODO",
                    "credit": "TODO",
                    "sourceUrl": "TODO"
                }
            ],
            "map": {
                "geoJson": "assets/geojson/lion-rock.geojson",  # TODO
                "zoom": 14.84,
                "center": {
                    "latitude": 22.352484,
                    "longitude": 114.185105
                }
            },
            "reference": url
        }
        englishUrl = url.replace('route.php', 'route_en.php')
        englishPageRequest = scrapy.Request(
            englishUrl, callback=self.parse_english_page)
        englishPageRequest.meta['trail'] = trail
        englishPageRequest.meta['area'] = area
        yield englishPageRequest

    def parse_english_page(self, response):
        area = response.meta['area']
        areaToRegion = {
            '0': 'Hong Kong Island',
            '1': 'Hong Kong Island',
            '2': 'Kowloon',
            '3': 'New Territories',
            '4': 'Hong Kong Island',
            '5': 'Hong Kong Island',
            '6': 'Hong Kong Island',
            '7': 'Islands',
            '8': 'Islands'
        }
        generalInfoEn = response.css(
            'div.generalInfo td::text').getall()
        englishTrail = {
            'name_en': generalInfoEn[0],
            'description_en': response.css('p.intro::text').get(),
        }
        region = {
            'name_en': areaToRegion[area],
        }
        district = {
            'name_en': response.css('p#indicator::text').get().split('\\')[2].strip(),
        }
        trail = response.meta['trail']
        trail['regions'] = merge(trail['regions'][0], region)
        trail['districts'] = merge(trail['districts'][0], district)
        yield merge(trail, englishTrail)
