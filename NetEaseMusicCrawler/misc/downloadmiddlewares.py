#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/29

import random
from NetEaseMusicCrawler.misc.useragents import USER_AGENTS


class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers['User-Agent'] = useragent
