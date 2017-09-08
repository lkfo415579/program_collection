# -*- coding: utf-8 -*-
import scrapy
import uniout
import codecs
import sys
from scrapy import Selector
class LEXICON_Spider(scrapy.Spider):
    
    name = "lexicon"
    website = "https://hk.lexiscn.com/"
    allowed_domains = ["hk.lexiscn.com"]
    
    
    #start = 1
    #loop = 36534040
    #

    def __init__(self, page='', *args, **kwargs):
        super(LEXICON_Spider, self).__init__(*args, **kwargs)
        start_urls = [
        "https://hk.lexiscn.com/latest_message.php?id="+page+"/"
        ]
        for i in range(int(page), 229638):
            self.start_urls.append("https://hk.lexiscn.com/latest_message.php?id="+str(i)+"/")
        self.runner = 0
    '''def parse(self, response):
        book_urls = response.selector.xpath('//p[@class="title"]/a/@href').extract()
        web = self.website
        print book_urls[:2]
        book_urls = [web+url for url in book_urls]
        for url in book_urls:
            yield scrapy.Request(url, callback=self.mid_parse)'''
            
    '''def handle_splited(self,html,option):
        #option,0 = off newline for firstline, 1 = on 
        output = []
        for line in html:
            sel = Selector(text=line, type="html")
            sen = sel.xpath('//text()').extract()
            #print line
            #print sen
            if option:
                sen[0] = sen[0]+"\n"
            output.append(''.join(sen))
        return [x.strip() for x in output]'''
    def ENG_parse(self, response):
        web = response.url
        runner = response.meta['runner']
        #title = response.selector.xpath('//h6[@id="news-subject"]//text()').extract()
        text = response.selector.xpath('//div[@class="news-article"]//text()').extract()
        text = self.BR_SPLITER(text)
        with codecs.open('hk_lexiscn.en', 'a','utf-8') as the_file:
            the_file.write("<doc id='"+str(runner)+"' >\n")
            #the_file.write("".join(title)+"\n")
            the_file.write("\n".join(text))
            the_file.write("\n</doc>\n")
        
    def BR_SPLITER(self,text): 
        #text[0].split('<br>')
        #print text
        #for line in text:
        #    if (line.strip() != ''):
        #        print line.strip()
        
        text = [line.strip() for line in text if line.strip() != '' ]
        return text
        
    def parse(self,response):
        web = response.url
        #time = response.selector.xpath('//div[@class="inline_block eight_col va_top"]//text()').extract()
        title = response.selector.xpath('//h6[@id="news-subject"]//text()').extract()
        #author = response.selector.xpath('//div[@class="contrib-group fm-author"]').extract()
        #abstract = response.selector.xpath('//div[@class="tsec sec"]').extract()
        text = response.selector.xpath('//div[@class="news-article"]//text()').extract()
        url = response.selector.xpath('//div[@class="news-article"]/a[@class="version_select"]/@href').extract()
        #version = response.selector.xpath('//a[@class="version_select"]/font//text()').extract()
        version = response.selector.xpath('//div[@class="news-article"]/a[@class="version_select"]//text()').extract()
        text = self.BR_SPLITER(text)
        #title = self.handle_splited(title,0)
        try:
            version = version[0]
        except:
            pass
        print "VERSION:",
        print version
        #print url
        #print "TEXT:",
        #print text
        
        if (version == u"英文版"):
            #print "GOT IT"
            writable = True
            self.runner += 1
        else:
            writable = False
        if (writable):
            with codecs.open('hk_lexiscn.zh', 'a','utf-8') as the_file:
                the_file.write("<doc id='"+str(self.runner)+"' >\n")
                #the_file.write("".join(title)+"\n")
                the_file.write("\n".join(text))
                the_file.write("\n</doc>\n")
            #go for eng page
            yield scrapy.Request(self.website[:-1]+url[0], callback=self.ENG_parse,meta={'runner': self.runner})
            #the_file.write("!"+time+"\n")
            '''the_file.write("$"+"".join(title)+"\n")
            the_file.write("@"+web +"\n")
            the_file.write("#"+"".join(author) +"\n")
            #the_file.write("\n".join(abstract))
            the_file.write("\n".join(text))
            the_file.write("\n")'''