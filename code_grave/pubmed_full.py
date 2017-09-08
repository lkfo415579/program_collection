import scrapy
import uniout
import codecs
import sys
from scrapy import Selector
class pubmed_FULL_Spider(scrapy.Spider):
    
    name = "pubmed_full"
    website = "https://www.ncbi.nlm.nih.gov/"
    allowed_domains = ["ncbi.nlm.nih.gov"]
    
    
    #start = 1
    #loop = 36534040
    #

    def __init__(self, page='', *args, **kwargs):
        super(pubmed_FULL_Spider, self).__init__(*args, **kwargs)
        start_urls = [
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC"+page+"/"
        ]
        for i in range(int(page), 5553803):
            self.start_urls.append("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC"+str(i).zfill(7)+"/")
    '''def parse(self, response):
        book_urls = response.selector.xpath('//p[@class="title"]/a/@href').extract()
        web = self.website
        print book_urls[:2]
        book_urls = [web+url for url in book_urls]
        for url in book_urls:
            yield scrapy.Request(url, callback=self.mid_parse)'''
            
    def handle_splited(self,html,option):
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
        return [x.strip() for x in output]
        
    def parse(self,response):
        web = response.url
        time = response.selector.xpath('//div[@class="inline_block eight_col va_top"]//text()').extract()
        title = response.selector.xpath('//h1[@class="content-title"]//text()').extract()
        author = response.selector.xpath('//div[@class="contrib-group fm-author"]').extract()
        #abstract = response.selector.xpath('//div[@class="tsec sec"]').extract()
        text = response.selector.xpath('//div[@class="tsec sec"]').extract()
        text = self.handle_splited(text,1)
        title = self.handle_splited(title,0)
        author = self.handle_splited(author,0)
        #abstract = self.handle_splited(abstract)
        
        #TEST
        try:
            time = time[-4]
        except:
            time = ""
        #print time
        #",".join(time)
        with codecs.open('pubmed_FULL_3.txt', 'a','utf-8') as the_file:
            the_file.write("!"+time+"\n")
            the_file.write("$"+"".join(title)+"\n")
            the_file.write("@"+web +"\n")
            the_file.write("#"+"".join(author) +"\n")
            #the_file.write("\n".join(abstract))
            the_file.write("\n".join(text))
            the_file.write("\n")