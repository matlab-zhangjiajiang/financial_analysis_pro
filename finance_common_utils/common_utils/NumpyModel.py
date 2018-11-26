#coding=utf-8
import numpy as np
##131页

arrayone =np.array(range(6))
viewone =arrayone.shape ##查看数据结构
arrayone.shape=2,3 ##将单行集合改变为2行3列 多维数组
arraytwo = arrayone.reshape(3,2) ##将单行集合变更为3行3列多维数组



print(arraytwo)
