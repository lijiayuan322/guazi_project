# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    car_id = scrapy.Field()
    car_name = scrapy.Field()
    from_url = scrapy.Field()
    car_price = scrapy.Field()
