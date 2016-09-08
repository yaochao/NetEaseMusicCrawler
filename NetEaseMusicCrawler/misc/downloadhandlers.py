#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/9/6
import Queue
import logging

from pydispatch import dispatcher
from scrapy import signals
from scrapy.responsetypes import responsetypes
from scrapy.signalmanager import SignalManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from twisted.internet import defer
from twisted.internet import threads
from twisted.python.failure import Failure

logger = logging.getLogger(__name__)


class PhantomJSDownloadHandler():
    def __init__(self, settings):
        self.options = settings.get('PHANTOMJS_OPTIONS', {})  # 默认空
        max_run = settings.get('PHANTOMJS_MAXRUN', 10)  # PhantomJS 可以同时运行最大的个数, 默认10
        self.sem = defer.DeferredSemaphore(max_run)
        self.queue = Queue.LifoQueue(maxsize=max_run)  # LifoQueue 后进先出队列
        SignalManager(dispatcher.Any).connect(receiver=self._close, signal=signals.spider_closed)

    def download_request(self, request, spider):
        ''' use semaphore to guard a phantomjs pool'''
        return self.sem.run(self._wait_request, request, spider)

    def _wait_request(self, request, spider):
        try:
            driver = self.queue.get_nowait()
        except:
            driver = webdriver.PhantomJS(**self.options)
        driver.get(request.url)

        # wait until ajax completed
        dfd = threads.deferToThread(self._wait_and_switch, driver)
        dfd.addCallback(self._response, driver, spider)
        return dfd

    def _response(self, _, driver, spider):
        body = driver.execute_script('return document.documentElement.innerHTML')
        if body.startswith(
                "<head></head>"):  # selenium 不能获取http相应的头信息,所以无法确定获取不成功的状态码,可以根据body的开头是佛为<head></head>来判断,是否请求成功
            body = driver.execute_script('return document.documentElement.textContent')
        url = driver.current_url
        respcls = responsetypes.from_args(url=url, body=body[:100].encode('utf-8'))
        response = respcls(url=url, body=body, encoding='utf-8')

        response_failed = getattr(spider, 'response_failed', None)
        if response_failed and callable(response_failed) and response_failed(response, driver):
            driver.quit()
            return defer.fail(Failure())
        else:
            self.queue.put(driver)  # 把driver重新放回queue
            return defer.succeed(response)  # 返回response对象

    def _wait_and_switch(self, driver):
        try:
            # wait
            element = WebDriverWait(driver=driver, timeout=10).until(
                expected_conditions.presence_of_element_located((By.ID, 'date_views')))
            # switch
            driver.switch_to.window(driver.current_window_handle)
        except:
            logger.error('timeout but ajax until not completed')

    def _close(self):
        '''清理工作: 把queue里面的driver全部关闭'''
        while not self.queue.empty():
            driver = self.queue.get_nowait()
            driver.quit()
