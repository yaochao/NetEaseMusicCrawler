# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

import pymongo
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class NeteasemusiccrawlerPipeline(object):
    def process_item(self, item, spider):
        print 'process_item'
        for key in item.keys():
            print item[key]


# 存储到Mongodb
class MongodbStorePipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client[settings['MONGO_DB']]
        self.collection = self.db[settings['MONGO_COLLECTION']]

    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger = logging.getLogger('MongodbStorePipeline')
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()
