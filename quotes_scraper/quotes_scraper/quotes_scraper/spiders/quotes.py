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
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['bustillo.al17@hotmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Juancho',
        'FEED_EXPORT_ENCODING': 'utf8'
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            authors = kwargs['authors']          
       
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        authors.extend(response.xpath('//span//small[@class="author" and @itemprop="author"]/text()').getall())
    
        quotes_author = [{'quote': quote, 'author': author} for  quote, author in zip(quotes, authors)]

        nex_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if nex_button_link:
            yield response.follow(nex_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors})
        else:
            yield {
                'quotes': quotes_author
            }            

    def parse(self, response):       
        title = response.xpath('//h1/a/text()').get()       
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        authors = response.xpath('//span//small[@class="author" and @itemprop="author"]/text()').getall()         
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()        

        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        yield {
            'title': title,            
            'top_tags': top_tags
        }

        next_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_button_link:
            yield response.follow(next_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors})

        
        # ONE PICE
        #title = response.xpath('//h1[@class="title-name"]/text()').get()
        #episodes = response.xpath('//td[@class="episode-title"]/a/text()').getall()
        

