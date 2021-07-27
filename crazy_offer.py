import scrapy


class CrazyOfferSpider(scrapy.Spider):
    name = 'crazy_offer'
    allowed_domains = ['www.cigabuy.com']
    start_urls = ['https://www.cigabuy.com/crazy-sales-c-56.html']

    def parse(self, response):
        for product in response.xpath("//div[@class='r_b_c']/div[@class='p_box_wrapper']"):
            
            yield {
                'title' : product.xpath(".//div/a[@class='p_box_title']/text()").get(),
                'url' : product.xpath(".//div/a[@class='p_box_title']/@href").get(),
                'discounted_price' : product.xpath(".//div[@class='p_box_price cf']/span[1]/text()").get(),
                'original_price' : product.xpath(".//div[@class='p_box_price cf']/span[2]/text()").get()
            }
        next_page = response.xpath("(//a[@class='nextPage']/@href)[1]").get()
        
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

