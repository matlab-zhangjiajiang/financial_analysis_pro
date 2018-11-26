#coding=utf-8

import numpy as np
import pandas as pd
import tushare as tu
import matplotlib.pyplot as plt

#####DataFrame功能讲解
data = tu.get_money_supply()

##M1,M2,M0图形展示
columns =['month','m2','m1','m0']
newdata = data[columns]
newdata = newdata[newdata['m2']!='--']
month = newdata.month.T.values
newindex=[]
for months in month:
    splitlist = str(months).split('.')
    yearsvar = splitlist[0]
    monthvar ='00'
    if len(splitlist[1])!=2:
        monthvar='0'+splitlist[1]
    else:
        monthvar=splitlist[1]
    newtime=yearsvar+'-'+monthvar+'-15'
    newindex.append(newtime)
m2=newdata.m2.T.values.astype(float)
m1=newdata.m1.T.values.astype(float)
m0=newdata.m0.T.values.astype(float)
newdata =pd.DataFrame({'m0':m0,'m1':m1,'m2':m2},index=pd.to_datetime(newindex))
newdata.plot()
plt.show()


###M1,M2,M3 同比增长
#pronewdata=newdata.shift(-1)
#growthrate = (newdata-pronewdata)/pronewdata
#growthrate.plot()
#plt.show()

###pd.concat([df,s1],axis=1) ###横向合并   页码156
###pd.appends(df) ###纵向合并
##1990.12
