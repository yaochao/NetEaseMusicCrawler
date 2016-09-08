#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/9/7

from scrapy.spiders import Spider


class NetEaseMusicSpider(Spider):
    name = 'demo'
    # start_urls = ['http://music.163.com/user/home?id=31888614']
    # start_urls = ['http://soft.coderabc.com/#!/detail/57b09c00043efa0ecff97492']
    start_urls = ['http://www.toutiao.com/']

    def parse(self, response):
        print response.body
        print response.url
