import scrapy 

# Titulo de la web = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags = //div[contains(@class, 'tags-box')]//span[@class="tag-item"]/a/text()
# Next page button = //ul[@class="pager"]//li[@class="next"]/a/@href

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        #'https://myanimelist.net/anime/21/One_Piece/episode'
    ]

    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json'
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

        nex_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if nex_button_link:
            yield response.follow(nex_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
        else:
            yield {
                'quotes': quotes
            }            

    def parse(self, response):       
        title = response.xpath('//h1/a/text()').get()       
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()        
        top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()        

        yield {
            'title': title,            
            'top_ten_tags': top_ten_tags
        }

        nex_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if nex_button_link:
            yield response.follow(nex_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})

        
        # ONE PICE
        #title = response.xpath('//h1[@class="title-name"]/text()').get()
        #episodes = response.xpath('//td[@class="episode-title"]/a/text()').getall()
        

