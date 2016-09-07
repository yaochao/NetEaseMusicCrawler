#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/9/6
import os
import tempfile

from scrapy.responsetypes import responsetypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class HttpDownloadHandler(object):
    def __init__(self, settings):
        service_args = [
            '--load-images=false',
            '--disk-cache=true',
            '--local-storage-path=%s' % os.path.join(tempfile.gettempdir(), 'phantomjs')
        ]
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', service_args=service_args)


        # chromeoptions = Options()
        # prefs = {
        #     'profile.managed_default_content_settings.images': 2
        # }
        # chromeoptions.add_experimental_option('prefs', prefs)
        # self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chromeoptions)

    def __del__(self):
        self.driver.quit()

    # TODO: 借助twisted的异步, 实现异步现在。
    # TODO: 如何关闭webdriver
    # TODO: 超时时间设置
    def download_request(self, request, spider):
        url = request.url
        print 'url....', url
        self.driver.get(url)
        status = 200
        cls = responsetypes.from_args(url=url)
        headers = None
        response = cls(url=url, status=status, headers=headers, request=request)
        request.meta['driver'] = self.driver
        return response
