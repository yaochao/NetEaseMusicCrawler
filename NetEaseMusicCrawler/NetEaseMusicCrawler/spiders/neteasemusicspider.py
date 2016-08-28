#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/28

from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor

class NetEaseMusicSpider(Spider):
    name = 'neteasemusic'
    allowed_domains = ['163.com']
    start_urls = ['http://music.163.com/#/user/home?id=31888614']

    def parse(self, response):
        print response.body