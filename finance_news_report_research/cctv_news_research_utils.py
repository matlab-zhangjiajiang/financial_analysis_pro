# coding=utf-8
import tushare as tu
import pandas as pd


# 设置PRO-API
tu.set_token("b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2")
pro = tu.pro_api()
class cctv_news_research_utils(object):

    def research_cctv_current_news(self):
          dfs = pro.news(src='sina', start_date='20181121', end_date='20181122')
          print(dfs)

if __name__ == '__main__':
    cctv_news_research_utils().research_cctv_current_news()