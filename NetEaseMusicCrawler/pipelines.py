# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NeteasemusiccrawlerPipeline(object):
    def process_item(self, item, spider):
        print 'process_item'
        for key in item.keys():
            print item[key]
