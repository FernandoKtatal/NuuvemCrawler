import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "steamgames" #Crawler name
    i = 0
    start_urls = [
        'https://store.steampowered.com/search/?category1=998',
    ]
    def parse(self, response):
        # gonna locate its price and check if it's a number or a string
        # if its a number put them together, if not put what is in the String (Free or Unavailable)
        # We use extract_first() so we won't get the item with the [ that comes with it 
        for steamgames in response.css('#search_result_container div a'): 
            priceTxt = steamgames.css('div div.search_price::text').extract_first()
            # removing the spaces if it's not a number
            priceTxt = re.sub(r"[\s]", "", priceTxt)
            if (priceTxt == "FreetoPlay"):
                priceTxt = "0,0"
            yield {
                'name': steamgames.css('div.search_name span.title::text').extract_first(),
                'price': priceTxt,
                'link': steamgames.css('::attr(href)').extract_first(),
                }
        # Goes to next item on the list with the links, so the crawler goes to the next page
        # self.i +=1
        # next_page = response.css('noscript a::attr(href)')[self.i].extract()
        # if next_page is not None:
        #     next_page = next_page
        #     yield scrapy.Request(next_page, callback=self.parse)


