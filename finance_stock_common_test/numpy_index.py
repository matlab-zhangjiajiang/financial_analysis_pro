#coding=utf-8
#NumPy：N维数组容器
#SciPy：科学计算函数库
#Pandas：表格容器 ,主要基于DataFrame
#Tushare + pyalgotrade + pandas

import numpy as num

print '使用列表生成一维数组'
data = [1,2,3,4,5,6]
x = num.array(data)
print x #打印数组
print x.ndim #打印数组的维度
print x.dtype #打印数组元素的类型

print '使用列表生成二维数组'
data = [[1,2],[3,4],[5,6]]
x = num.array(data)
print x #打印数组
print x.ndim #打印数组的维度
print x.shape #打印数组各个维度的长度。shape是一个元组