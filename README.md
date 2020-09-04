# Hong Kong Hiking Routes Spider
This spider crawls Hong Kong hiking routes information from website and convert them into a single json file. 

## Run crawler
`scrapy crawl routes`

## Run scrapy shell
`scrapy shell 'http://www.walkonhill.com/route.php?area=1&seq=1'`

## Output result as a json
`rm -f trail-data.json && scrapy crawl routes -o trail-data.json`

Reference
- https://docs.scrapy.org/en/latest/intro/tutorial.html
- http://www.walkonhill.com/route.php?area=1&seq=1
