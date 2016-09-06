#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/9/6

from scrapy.responsetypes import responsetypes
from selenium import webdriver


class HttpDownloadHandler(object):
    def __init__(self, settings):
        # self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

    def __del__(self):
        self.driver.quit()

    # TODO: 借助twisted的异步, 实现异步现在。
    def download_request(self, request, spider):
        # url = urldefrag(request.url)[0]
        url = request.url
        print 'url....', url
        self.driver.get(url)
        status = 200
        cls = responsetypes.from_args(url=url)
        headers = None
        response = cls(url=url, status=status, headers=headers, request=request)
        request.meta['driver'] = self.driver
        return response
