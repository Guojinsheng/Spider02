from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# 就是一个普通的Scrapy爬虫，不是Scrapy-redis

class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'mybaike1'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/Python/407313']

    rules = [
        Rule(LinkExtractor(
            restrict_css=('.top-cat', '.sub-cat', '.cat-item')
        ), callback='parse_directory', follow=True),
    ]

    def parse_directory(self, response):
        for div in response.css('.title-and-desc'):
            yield {
                'name': div.css('.site-title::test').extract_first(),
                'description': div.css('.site-descr::test').extract_first().strip(),
                'link': div.css('a::attr(href)').extract_first(),
            }
