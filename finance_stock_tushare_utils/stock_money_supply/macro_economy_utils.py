#coding=utf-8
import pandas as pd
import numpy as np
import tushare as tu
import matplotlib as mt

class macroeconomyutils(object):


    def getmoneysupply(self):
        data = tu.get_money_supply()
        data.rename(columns={'m2_yoy':'M2同比增长(%)','m1_yoy':'M1同比增长(%)','m0_yoy':'M0同比增长(%)','cd':'活期存款(亿元)',
                             'qm':'准货币(亿元)','ftd':'定期存款(亿元)','sd':'储蓄存款(亿元)','rests':'其他存款(亿元)'},inplace=True)
        data.replace('0','--')
        return data



if __name__ == '__main__':
        print(macroeconomyutils().getmoneysupply())