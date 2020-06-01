# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from mongodb import Mongo


class GuaziProjectPipeline:
    def process_item(self, item, spider):
        data = dict(item)
        mongo = Mongo()
        mongo.save_many(data)
        return item
