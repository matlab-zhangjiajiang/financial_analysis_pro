#coding=utf-8
import pandas as pd
import numpy as np
import tushare as tu
import matplotlib as mt

class stock_pledge_infor(object):
    """
    股票质押数据
    return DataFrame
    --------------
    code: 证券代码
    name: 证券名称
    deals: 质押次数
    unrest_pledged: 无限售股质押数量(万)
    rest_pledged: 限售股质押数量(万)
    totals: 总股本
    p_ratio:质押比例（%） 按降序排列
    """
    def get_all_stock_pledged(self):
        return tu.stock_pledged().sort_values(['p_ratio'],ascending=False)


    ##df['code'] = df['code'].map(lambda x :str(x).zfill(6))
    # 改为: df['code'] = df['code'].map(lambda x :str(x).rjust(6,'0'))
    """
    股票质押数据
    return DataFrame
    --------------
    code: 证券代码
    name: 证券名称
    ann_date: 公告日期
    pledgor:出质人
    pledgee:质权人
    volume:质押数量
    from_date:质押日期
    end_date: 解除日期
    """
    def get_all_stock_pledge_detail(self,name):
        data = tu.pledged_detail().sort_values(['from_date'],ascending=False)
        return data.loc[data['name']==name]

    ##pdata 返回质押股份的明细信息
    ##average_value 返回的质押股份的平均值
    def get_stock_pledge_times(self,name):
        data =stock_pledge_infor().get_all_stock_pledge_detail(name)
        datab = data.groupby(['name'])
        newdata = datab.count().sort_values(['volume'],ascending=False)
        count = int(newdata.count()['volume'])
        names = list(newdata.index)
        namecount = list(newdata['volume'])
        sumcount = 0
        for num in namecount:
            sumcount+=int(num)
        pdata = pd.DataFrame({'name':names,'count':namecount},index=np.arange(count))
        return {'pdata':pdata,'average_value':sumcount/count}


if __name__ == '__main__':
    data = stock_pledge_infor().get_all_stock_pledge_detail('海翔药业')
    #data = stock_pledge_infor().get_stock_pledge_times('宗申动力')['pdata']
    print(data)
