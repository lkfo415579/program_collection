# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from crawler.items import CrawlerItem
from crawler.utils import get_first

class EEESpider(CrawlSpider):
    name = 'xich'
    #rotate_user_agent = True
    allowed_domains = ['xichuanpoetry.com']
    start_urls = ['http://xichuanpoetry.com/']
    rules = (
        Rule(
            LinkExtractor(
                #allow=('cipherjournal\.com\/([-\w]+\/)*([-\w]+)?(\?page\=.*)?$'),
                allow=('.*'),
            ),
            follow=True,
            callback='parse_page',
        ),
    )

    def parse_page(self, response):
        text = []
        for s in response.xpath('//text()').extract():
            if s.strip() != "":
                text.append(s.strip())
        if text:
            print "@@@@@@",response.url
            #print text
            item = CrawlerItem()
            item['url'] = response.url
            item['title'] = get_first(response.xpath('//title//text()').extract())
            item['text'] =  text
            return item
        else:
            pass