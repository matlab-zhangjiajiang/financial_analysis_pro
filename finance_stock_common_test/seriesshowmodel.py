#coding=utf-8

import numpy as np
import pandas as pd
import tushare as tu
import matplotlib.pyplot as plt
from datetime import datetime


data=['2018-01-01','2018-01-02','2018-02-03','2018-02-04','2018-03-05']
newdata =pd.Series([1,2,3,4,5],index=pd.to_datetime(data))
###时间范围内的检索
filterdata = newdata['2018-01':'2018-02']

####按月截取
##print(newdata['2018-01'])

###过滤条件筛选[]
data = newdata.truncate(after='2018-02-03')

###高低频时间序列转换(日线数据转换为月线数据)
datas = newdata.resample('M').first() ##'M'每月最后一天,'MS'每月的第一天
print(datas)


###计算每天的收益率问题
###newdata.shift(1) 正数为滞后
###newdata.shift(-1)  负数为超前
syl =(newdata-newdata.shift(1))/newdata.shift(1)
##print(syl)




