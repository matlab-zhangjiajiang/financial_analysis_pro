# coding=utf-8
from __future__ import division  # #保留两整数相除取浮点数
import pandas as pd
import tushare as tu


class stockclassifyutils(object):

    def __init__(self):
        self.stockbasic = tu.get_stock_basics()
        self.conceptclass=tu.get_concept_classified()

    ##获取概念信息
    def conceptstockclassify(self):
        data = self.conceptclass ##获取概念信息
        newdata = data.groupby(['c_name'],as_index=False).count()
        del newdata['code']  ##删除当前序列中的CODE列
        del newdata['name']  ##删除当前徐柳中的NAME列
        return newdata

    ###根据概念查询出对应的股票列表,并返回相应的股票基本面信息.
    def conceptstocklist(self,c_name):
        data =self.conceptclass
        print('根据当前['+c_name+']概念,获取的股票信息列表如下')
        newdata = data.loc[data['c_name']==c_name]
        codelist = list(newdata['name'])
        sortdata = None
        for name in codelist:
            data = self.stockbasic
            newdata= data.loc[(data['name']==name)&(data['pe']>0)&(data['pb']>0),['name','pe','pb','npr','holders','bvps','industry']]
            newdata['concept']=c_name
            sortdata = pd.concat([sortdata,newdata]) ###合并pandas
        return sortdata

    ###获取每个概念板块对应的股票信息
    def conceptconcatdata(self,num):
        data = stockclassifyutils().conceptstockclassify()
        returndata = None
        for name in list(data['c_name']):
            newdata = stockclassifyutils().conceptstocklist(name)
            cdata = newdata.sort_values(['pe','pb','npr','holders'],ascending=[True,True,False,True]).head(num)
            returndata = pd.concat([returndata,cdata])
        return returndata

if __name__ == '__main__':
    print(stockclassifyutils().conceptconcatdata(100))