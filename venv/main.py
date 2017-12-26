import scrapy

class BrickSetSpider(scrapy.Spider):
    name = 'brick_spider'
    start_urls = ['https://www.coinschedule.com/']

    def parse(self, response):
        SET_SELECTOR = '.link'
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'td a ::text'
            LINK_SELECTOR = 'td a ::attr(href)'
            #MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            #IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'link': brickset.css(LINK_SELECTOR).extract_first(),
            }