# Hong Kong Hiking Routes Spider
This spider crawls Hong Kong hiking routes information from website and convert them into json and geojosn files. 

## Settings
### Wait 250ms every request
`DOWNLOAD_DELAY = 0.25`

## Run crawler
`scrapy crawl routes`

## Run scrapy shell
`scrapy shell 'http://www.walkonhill.com/route.php?area=1&seq=1'`

## Output result as a json
`rm -f ./kml/**.* && rm -f ./geojson/**.* && rm -f trail-data.json && scrapy crawl routes -o trail-data.json`

## Convert kml to geojson
### kml2geojson lib
`pip install kml2geojson`
### Convert
`k2g ./kml/13.kml ./geojson`

## Get latitude and longtitude by place
- Get API key from https://opencagedata.com/dashboard#api-keys
- `pip install opencage`
- Set API key as ENV variable `export OPENCAGE_API_KEY=XXX`
- verify it by `echo $OPENCAGE_API_KEY`
- Follow steps in https://opencagedata.com/tutorials/geocode-in-python

## Reference
- https://docs.scrapy.org/en/latest/intro/tutorial.html

## Credits
- http://www.walkonhill.com
