# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 夏普比率研究
# 样本平均收益率 / 样本收益率标准差
import pandas as pd
import numpy as np

# 构建两个收盘价序列，都是从10涨到10.5, 但数据2显然质量更高

s1_c = pd.Series([10, 9.7, 10, 10.3, 10, 9.7, 10, 10.3, 10.5])
s2_c = pd.Series([10, 10.05, 10.1, 10.15, 10.2, 10.25, 10.3, 10.4, 10.5])

# 计算对数收益率序列
s1_rets = np.log(s1_c / s1_c.shift(1))
s2_rets = np.log(s2_c / s2_c.shift(1))

# 计算平均收益率
s1_rets_mean = s1_rets.mean()
s2_rets_mean = s2_rets.mean()

print('平均收益率:', s1_rets_mean, s2_rets_mean)
print('收益率标准差:', s1_rets.std(), s2_rets.std())

# 计算夏普比率
s1_sharp_ratio = s1_rets_mean / s1_rets.std()
s2_sharp_ratio = s2_rets_mean / s2_rets.std()

print('夏普比率:', s1_sharp_ratio, s2_sharp_ratio)