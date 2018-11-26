#coding=utf-8
from __future__ import division   ##保留两整数相除取浮点数
import pandas as pd
import tushare as tu
import matplotlib.pyplot as plt
###数据模型具体思路：获取所有的股票信息,[按照行业分组],[净利润率算平均,股东数汇总,市盈率平均],[股东数升序,净利润率降序]
stockdata = tu.get_stock_basics()
dict_map = {'npr':'mean','holders':'sum','pe':'mean'}
data = stockdata.groupby(['industry'],as_index=False)\
    .agg(dict_map)\
    .sort_values(['holders','npr'],ascending=[True,False])
data['holders'] = [holds/100000 for holds in list(data['holders'])]
data.rename(columns={'industry':'行业','holders':'股东数(十万)','npr':'净利润率','pe':'平均市盈率'},inplace=True)
#print(data.head(20))
data.to_excel('IndustryAverageProfit.xlsx')

