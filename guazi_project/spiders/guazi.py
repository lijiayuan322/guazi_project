# -*- coding: utf-8 -*-
import re

import scrapy

from mongodb import Mongo
from ..items import GuaziProjectItem


class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['guazi.com']
    # start_urls = ['http://guazi.com/']

    def __init__(self):
        super(GuaziSpider,self).__init__()
        self.mongo = Mongo()

    def start_requests(self):
        """开始的url"""
        while True:
            data = self.mongo.get_data()
            if data:
                url = data.get('url')
                data['url'] = url.replace("#bread","o{}i7/#bread".format(1))
                data.pop('_id')
                yield scrapy.Request(url=data['url'],
                                     callback=self.parse,dont_filter=True,
                                     errback=self.handle_err,meta={'data':data})
            else:
                break

    def parse(self, response):
        #返回的HTML 文本
        response_text = response.text
        if '中为您找到0辆好车' in response_text:
            return

        url_list = response.xpath("//ul[@class='carlist clearfix js-top']/li/a/@href").extract()
        for car_url in url_list:
            #找到页面每辆车的url
            response.request.meta['car_url'] = "https://www.guazi.com" + str(car_url)
            yield scrapy.Request(url=response.request.meta['car_url'],
                                 callback=self.handle_car_url,
                                 meta=response.request.meta,
                                 dont_filter=True,errback=self.handle_err)
        if response.xpath("//ul[@class='pageLink clearfix']/li[last()]/a/span/text()").extract_first() == '下一页':
            url = response.request.meta['data']['url']
            p = re.compile(r"https://www.guazi.com/.*?/.*?/o(\d+)i7/#bread")
            page_now = p.search(url).group(1)
            url = url.replace("o{}".format(page_now),"o{}".format(int(page_now)+1))
            response.request.meta['data']['url'] = url
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 dont_filter=True,
                                 errback=self.handle_err,meta=response.request.meta)


    def handle_car_url(self,response):
        car_url = response.request.meta.get("car_url")
        guaziprojectitem = GuaziProjectItem()
        #获取车源号正则
        id_p = re.compile(r'车源号：(.*?)\s+')
        #HTML文本
        text = response.text
        #车源号
        guaziprojectitem['car_id']= id_p.search(text).group(1)
        #车标题
        guaziprojectitem['car_name'] = response.xpath("//h2[@class='titlebox']/text()").extract_first().strip()
        guaziprojectitem['from_url'] = car_url
        guaziprojectitem['car_price'] = response.xpath("//span[@class='price-num']/text()").extract_first().strip()
        yield guaziprojectitem


    def handle_err(self,failure):
        data = failure.request.meta.get('data')
        if data:
            self.mongo.save(data)
