#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/28

import copy

from scrapy.http import Request
from scrapy.spiders import Spider

from NetEaseMusicCrawler.items import NeteasemusicItem


class NetEaseMusicSpider(Spider):
    name = 'neteasemusic'
    start_urls = ['http://music.163.com/user/home?id=31888614']
    faild_id = set()
    x_query = {
        'name': '//dd/div/div/h2/span[1]/text()',
        'level': '//dd/div[1]/div/h2/span[2]/text()',
        'header': '/html/body/div[3]/div/dl/dt/img/@src',
        'sex': '//dd/div[1]/div/h2/i/@class',
        'is_v': '',  # 是否认证
        'v_text': '',  # 认证资料
        'shares_count': '//dd/ul/li[1]/a/strong/text()',  # 动态数
        'followings_count': '//dd/ul/li[2]/a/strong/text()',  # 关注数
        'followers_count': '//dd/ul/li[3]/a/strong/text()',  # 粉丝数
        'followings': '',  # 正在关注
        'followers': '',  # 粉丝
        'introduction': '//div[@class="inf s-fc3 f-brk"]/text()',  # 个人介绍
        'region': '//div[@class="inf s-fc3"]/span[1]/text()',  # 地区
        'age': '//div[@class="inf s-fc3"]/span[2]/span/text()',  # 年龄
        'sns': '//dd/div[4]/ul/li',  # 社交网络
        'all_songs_count': '//div[@id="m-record"]/@data-songs',  # 累计收听歌曲数
        'week_songs_rank': '',  # 最近一周收听排行
        'all_songs_rank': '',  # 所有时间收听排行
        'url': '',
    }

    def parse(self, response):
        ''' parse the profile '''
        url = response.url
        _id = url.split('=')[-1]
        driver = response.meta['driver']
        item = NeteasemusicItem()

        try:
            driver.switch_to.default_content()
            g_iframe = driver.find_elements_by_tag_name('iframe')[0]
            driver.switch_to.frame(g_iframe)
            item['_id'] = _id
            item['header'] = driver.find_element_by_xpath('//dt[@id="ava"]/img').get_attribute('src')
            item['name'] = driver.find_element_by_xpath('//h2/span[1]').text
            item['level'] = driver.find_element_by_xpath('//h2/span[2]').text
            sex = driver.find_element_by_xpath('//h2/i').get_attribute('class')
            sex = '1' if sex == 'icn u-icn u-icn-01' else '0'
            item['sex'] = sex
            item['shares_count'] = driver.find_element_by_xpath('//*[@id="event_count"]').text
            item['follows_count'] = driver.find_element_by_xpath('//*[@id="follow_count"]').text
            item['fans_count'] = driver.find_element_by_xpath('//*[@id="fan_count"]').text

            try:
                item['introduction'] = driver.find_element_by_xpath('//div[@class="inf s-fc3 f-brk"]').text
            except:
                item['introduction'] = None

            try:
                item['region'] = driver.find_element_by_xpath('//div[@class="inf s-fc3"]/span').text
            except:
                item['region'] = None

            try:
                item['age'] = driver.find_element_by_xpath('//*[@id="age"]/span').text
            except:
                item['age'] = None

            try:
                snss = driver.find_elements_by_xpath('//ul[@class="u-logo u-logo-s f-cb"]/li')
                sns = []
                for s in snss:
                    try:
                        a = s.find_element_by_tag_name('a')
                        title = a.get_attribute('title')
                        href = a.get_attribute('href')
                        sns.append({title: href})
                    except Exception as e:
                        print e
                item['sns'] = sns
            except:
                item['sns'] = None

            try:
                all_songs_count = driver.find_element_by_xpath('//*[@id="rHeader"]/h4').text
                all_songs_count = all_songs_count[4:][:-1]
                item['all_songs_count'] = all_songs_count
            except:
                item['all_songs_count'] = None
        except Exception as e:
            # 说明请求失败,把id加入到失败的set里面
            self.faild_id.add(_id)
            print e

        # driver.close()
        request = Request(url='http://music.163.com/user/follows?id=' + _id, callback=self.parse_follows)
        request.meta['item'] = copy.deepcopy(item)
        yield request

    def parse_follows(self, response):
        ''' parse the follows '''
        url = response.url
        _id = url.split('=')[-1]
        item = response.meta['item']
        driver = response.meta['driver']
        try:
            driver.switch_to.default_content()
            g_iframe = driver.find_elements_by_tag_name('iframe')[0]
            driver.switch_to.frame(g_iframe)
            lis = driver.find_elements_by_xpath('//*[@id="main-box"]/li')
            follows = {}
            for li in lis:
                a = li.find_element_by_tag_name('a')
                title = a.get_attribute('title')
                href = a.get_attribute('href')
                uid = href.split('=')[-1]
                follows[uid] = title
            item['follows'] = follows
        except Exception as e:
            print e

        # driver.close()
        request = Request(url='http://music.163.com/user/fans?id=' + _id, callback=self.parse_fans)
        request.meta['item'] = copy.deepcopy(item)
        yield request

    def parse_fans(self, response):
        ''' parse the follows '''
        url = response.url
        _id = url.split('=')[-1]
        item = response.meta['item']
        driver = response.meta['driver']
        try:
            driver.switch_to.default_content()
            g_iframe = driver.find_elements_by_tag_name('iframe')[0]
            driver.switch_to.frame(g_iframe)
            lis = driver.find_elements_by_xpath('//*[@id="main-box"]/li')
            fans = {}
            for li in lis:
                a = li.find_element_by_tag_name('a')
                title = a.get_attribute('title')
                href = a.get_attribute('href')
                uid = href.split('=')[-1]
                fans[uid] = title
            item['fans'] = fans
        except Exception as e:
            print e

        # driver.close()
        request = Request(url='http://music.163.com/user/songs/rank?id=' + _id, callback=self.parse_songs_rank)
        request.meta['item'] = copy.deepcopy(item)
        print item
        yield request

    def parse_songs_rank(self, response):

        pass
