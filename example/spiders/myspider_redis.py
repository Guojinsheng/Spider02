from scrapy_redis.spiders import RedisSpider

from example.items import BaikeItem


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    # 爬虫名
    name = 'mybaikespider_redis'
    # redis_key： 类似start_url,但是只是redis的一个key
    # 监听当前爬虫所连接的redis数据库中的指定key为‘myspider:start_urls’是否改变
    redis_key = 'mybaikespider:start_urls'
    # 允许的域名
    allowed_domains = ['baike.baidu.com']


    def parse(self, response):
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
