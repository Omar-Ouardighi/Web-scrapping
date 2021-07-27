import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"))
    )

    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[@class='TitleBlock__Container-sc-1nlhx7j-0 hglRHk']/div/h1/text()").get(),
            'year': response.xpath("//div[@class ='TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr']/ul/li[1]/span/text()").get(),
            'duration': response.xpath("//div[@class ='TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr']/ul/li[3]/text()").get(),
            'rating': response.xpath("//span[@class ='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV']/text()").get(),
            'movie_url' : response.url
        }

        
