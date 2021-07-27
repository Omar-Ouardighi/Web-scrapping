import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which


class UsmayorSpider(scrapy.Spider):
    name = 'usmayor'
    allowed_domains = ['www.usmayors.org/mayors/meet-the-mayors']
    start_urls = [
        'https://www.usmayors.org/mayors/meet-the-mayors'
    ]


    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')

        chrome_path = which('chromedriver')

        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.get('https://www.usmayors.org/mayors/meet-the-mayors/')

        input_field = driver.find_element_by_xpath("//form[@id='searchform']/input[1]")
        input_field.send_keys('california')
        input_field.send_keys(Keys.ENTER)

        self.html = driver.page_source
        driver.close()

    

    def parse(self, response):
        resp = Selector(text=self.html)

        for mayor in resp.xpath("//div[@class='post-content']/ul"):
            yield {

                'mayor_name' : mayor.xpath('.//b/text()').get(),
                'city' : mayor.xpath("(.//text()[preceding-sibling::br and following-sibling::br])[1]").get(),
                'telephone' :mayor.xpath('.//a[3]/text()').get(),
                'email' :mayor.xpath('.//a[4]/text()').get()
                

            }

    
