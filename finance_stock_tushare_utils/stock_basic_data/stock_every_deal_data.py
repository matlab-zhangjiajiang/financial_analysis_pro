# coding=utf-8

import tushare as tu
import pandas as pd

class stock_every_deal_data(object):

    #统计每个价位的买与卖
    def analysis_every_deal_buyorsell(self):
        currentdata = tu.get_latest_news()
        print(currentdata)

        print(currentdata)
        if(currentdata is None):
            print('为空')


if __name__ == '__main__':
    stock_every_deal_data().analysis_every_deal_buyorsell()
