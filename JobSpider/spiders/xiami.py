# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from JobSpider.items import JobspiderItem

class XiamiSpider(scrapy.Spider):
    name = 'xiami'
    allowed_domains = ['www.xiami.com']
    # start_urls = ['http://www.xiami.com/artist/iim17edb/']
    # start_urls = ['http://localhost/test/zhoujielun.html']
    start_urls = ['https://www.xiami.com/list?scene=artist&type=album&query={%22artistId%22:%221260%22}']
    

    def parse(self, response):
        print('----------parse--------')

        with open('xiami.html','wb') as f:
            f.write(response.body)
            pass
        # lists = response.css('.related-albums .album-item')
        lists = response.css('.adaptive-list .album-item')
        item = JobspiderItem()
        for list in lists:
            item['album_url'] = list.css('.name a::attr(href)').extract_first()
            item['album_name'] = list.css('.name a::text').extract_first()
            item['author'] = list.css('.author a::text').extract_first()
            item['grade'] = list.css('.grade-num::text').extract_first()
            item['time'] = list.css('.time::text').extract_first()

            yield item
            pass
        pageLists = response.css('.rc-pagination .rc-pagination-item')
        print('pageLists',pageLists)
        print('len',len(pageLists))

        for pagelist in pageLists:
            url = pagelist.css('a::attr(href)').extract_first()
            url_full = 'https://www.xiami.com%s' %(url)
            print('开始新的一页',url_full)
            yield Request(url=url_full, callback=self.parse)
        pass
