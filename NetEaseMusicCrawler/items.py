# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field


class NeteasemusicItem(Field):
    _id = Field()  # user id as a mongodb item's _id
    name = Field() # 昵称
    header_img = Field() # 头像
    sex = Field() # 性别
    is_v = Field() # 是否认证
    v_text = Field() # 认证资料
    followers = Field() # 粉丝
    followers_count = Field() # 粉丝数
    followings = Field() # 正在关注
    followings_count = Field() # 关注数
    shares_count = Field() # 动态数
    introduction = Field() # 个人介绍
    region = Field() # 地区
    age = Field() # 年龄
    sns = Field() # 社交网络
    all_songs_count = Field() # 累计收听歌曲数
    week_songs_rank = Field() # 最近一周收听排行
    all_songs_rank = Field() # 所有时间收听排行
    url = Field()
