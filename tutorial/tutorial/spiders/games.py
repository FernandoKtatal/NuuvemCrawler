import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "games"
    i = 0
    start_urls = [
        'https://www.nuuvem.com/catalog',
    ]

    def parse(self, response):

        for game in response.css('div.product-card--grid'):
            price1 = game.css('span span.integer::text').extract_first()
            price2 = game.css('span span.decimal::text').extract_first()
            priceTxt = game.css('span.product-price--val::text').extract_first()
            
            if price1 is None:
                price1 = re.sub(r"[\s]", "", priceTxt)
            else:
                price1 = price1+price2
            yield {
                'name': game.css('h3.product-title::text').extract_first(),
                'price': price1,
                'link': game.css('a.product-card--wrapper::attr(href)').extract_first()
            }
            
        self.i +=1
        next_page = response.css('noscript a::attr(href)')[self.i].extract()
        if next_page is not None:
            next_page = next_page
            yield scrapy.Request(next_page, callback=self.parse)


