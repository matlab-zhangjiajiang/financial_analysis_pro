# coding=utf-8
from __future__ import division  # #保留两整数相除取浮点数
import tushare as tu
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
import sqlalchemy

class stockbasicsideutils(object):


    def getstockbasicby_pe_pb(self):
        data = tu.get_stock_basics()
        newdata = data.sort_values(['pe','pb','holders'],ascending=[True,True,True])
        ##PE必须大于零,PB大于零
        returndata = newdata.loc[(newdata['pe']>0)&(newdata['pb']>0),['name','pe','pb','holders']]
        #createdata = pd.DataFrame({'pe':list(newdata['pe']),'pb':list(newdata['pb']),'name':list('name')},index=list(newdata.index))
        return returndata

    #低于每股净资产的股票.
    #按照PE,和股东数降序排序得到如下结果
    def getlowerthanstocknetassets(self):
        data = tu.get_stock_basics()
        return data.loc[(data['pe']>0)&(data['pb']<1)&(data['pb']>0),['name','pe','pb','holders']].sort_values(['pe','holders'],ascending=[True,True])

    ##低于每股净资产的股票数.
    def query_lower_pb_stock_infor(self):
        data = tu.get_stock_basics()
        return data.loc[(data['pb']<1),['name']].count()


    #生猪行业,按照市盈率,PB,净利润增长率,股东人数来去排序筛选
    def getanalysisofpigindustry(self,industry):
        data = tu.get_stock_basics()
        return data.loc[(data['industry']=='农业综合')&(data['pb']>0)&(data['pe']>0),['name','pe','pb','npr','holders']].sort_values(['pe','pb','npr','holders'],ascending=[True,True,False,True])

    def getbasicimportantinfor(self):
        data = tu.get_report_data(year=2017,quarter=4)
        print data

if __name__ == '__main__':
    #engine = dbmanager.sql_manager().init_engine()
    #data = tu.get_notices()
    #print(data.T)
    #data.to_sql('pe_pb_stock_infor',engine,if_exists='replace')
    print(stockbasicsideutils().query_lower_pb_stock_infor())
