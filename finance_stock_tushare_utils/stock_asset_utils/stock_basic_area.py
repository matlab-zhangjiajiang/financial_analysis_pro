#coding=utf-8
import pandas as pd
import tushare as tu

pds=tu.get_stock_basics()
pds.to_excel('stock_basic_data.xlsx')
dict_map = {'esp':'mean'}
data = pds.groupby(['area'],as_index=False).agg(dict_map).sort_values(['esp'],ascending=[False])
data.rename(columns={'area':'地域','esp':'平均每股收益'},inplace=True)
data.to_excel('area_average_income.xlsx')