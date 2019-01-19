from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider
from example.items import BaikeItem
# from ..items import BaikeItem

'''
运行后会自动在redis生成一些key：
    mybaikecrawler_redis:items : 爬取的数据
    mybaikecrawler_redis:requests : 待爬取的request队列
    mybaikecrawler_redis:dupefilter: 重复的request，作用是去重
'''



class MyCrawler(RedisCrawlSpider):

    # 爬虫名
    name = 'mybaikecrawler_redis'
    # redis_key： 类似start_url,但是只是redis的一个key
    # 监听redis中的key
    redis_key = 'mybaikecrawler:start_urls'
    # 允许的域名
    allowed_domains = ['baike.baidu.com']

    # 全网爬取
    rules = [
        Rule(
            LinkExtractor(
                allow=('/item/.*',),
            ),
            callback='parse_item',
            follow=True
        )
    ]

    def parse_item(self, response):
        title = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').get()
        title = title if title else "主标题"
        sub_title = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h2/text()').get()
        sub_title = sub_title if sub_title else "副标题"
        content = response.xpath('//div[@class="lemma-summary"]/div/text()').get()
        content = content if content else "没有内容"

        print(title, sub_title)

        item = BaikeItem()
        item['title'] = title
        item['sub_title'] = sub_title
        item['content'] = content
        yield item
