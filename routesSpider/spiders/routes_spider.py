import scrapy
import math
import urllib.parse as urlparse
from urllib.parse import parse_qs


class QuotesSpider(scrapy.Spider):
    name = "routes"
    start_urls = [
        'http://www.walkonhill.com/route.php?area=1&seq=1',
        # 'http://www.walkonhill.com/route.php?area=1&seq=2',
        # http://www.walkonhill.com/route_en.php?area=1&seq=1 // following link?
    ]
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

    def parse(self, response):
        url = response.url
        queryString = parse_qs(urlparse.urlparse(url).query)
        area = queryString['area'][0]
        paths = response.css('div#trackpointList ol li a::text').getall()
        generalInfo = response.css(
            'div.generalInfo td.right_td::text').getall()
        yield {
            'name': generalInfo[0],
            'name_en': 'XXX TODO',
            'description': response.css('p.intro::text').get(),
            'description_en': 'XXX TODO',
            'region': [{
                'name': self.areaToRegion[area],
                'name_en': 'XXX TODO'
            }],
            'districts': [{
                'name': response.css('p#indicator::text').get().split('\\')[2].strip(),
                'name_en': 'XXX TODO'
            }],
            'height': -1,  # TODO
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
