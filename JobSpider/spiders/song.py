# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from JobSpider.items import SongspiderItem

class XiamiSpider(scrapy.Spider):
    name = 'song'
    allowed_domains = ['www.xiami.com']
    # start_urls = ['http://www.xiami.com/artist/iim17edb/']
    # start_urls = ['http://localhost/test/zhoujielun.html']
    # start_urls = ['https://www.xiami.com/list?spm=a2oj1.13847458.0.0.15745125Qrf5eV&query=%7B%22artistId%22%3A%221260%22%7D&scene=artist&type=song&page=3']
    baseURL='https://www.xiami.com/list?spm=a2oj1.13847458.0.0.15745125Qrf5eV&query=%7B%22artistId%22%3A%221260%22%7D&scene=artist&type=song&page='
    offset=1
    start_urls=[baseURL+str(offset)]

    def parse(self, response):
        print('----------parse--------')

        with open('xiami.html','wb') as f:
            f.write(response.body)
            pass
        # lists = response.css('.related-albums .album-item')
        lists = response.css('.list-song tbody tr')
        item = SongspiderItem()
        for list in lists:
            item['song_url'] = list.css('.song-name a::attr(href)').extract_first()#歌曲地址
            item['song_name'] = list.css('.song-name a::text').extract_first()#歌曲名称
            item['singers_url'] = list.css('.singers a::attr(href)').extract_first()#歌手地址
            item['singers'] = list.css('.singers a::text').extract_first()#歌手名称
            item['album_url'] = list.css('.album a::attr(href)').extract_first()#专辑地址
            item['album'] = list.css('.album a::text').extract_first()#专辑名称
            item['duration'] = list.css('.duration::text').extract_first()#时常
            

            yield item
            pass
        # pageLists = response.css('.rc-pagination .rc-pagination-item')
        # print('pageLists',pageLists)
        # print('len',len(pageLists))

        # for pagelist in pageLists:
        #     url = pagelist.css('a::attr(href)').extract_first()
        #     url_full = 'https://www.xiami.com%s' %(url)
        #     print('开始新的一页',url_full)
        #     yield Request(url=url_full, callback=self.parse)
        # pass
        if self.offset<=18:
            self.offset+=1
            url=self.baseURL+str(self.offset)
            yield scrapy.Request(url,callback=self.parse)

