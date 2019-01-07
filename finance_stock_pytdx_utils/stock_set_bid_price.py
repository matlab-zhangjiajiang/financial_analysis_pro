#coding=utf-8
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
from finance_stock_dao_model import stock_infor_base_dto as basicvo
from finance_stock_dao_model.stock_set_bid_base_dto import stock_set_bid_base_dto as dto
from connection_host_server import connection_host_server as serviceinfo
from finance_common_utils.common_utils import datetime_utils
import finance_common_utils.mysql_dbutils.sqlalchemy_dbutils as dbmanager
from finance_stock_dao_model.stock_set_bid_base_rate_dto import stock_set_bid_base_rate_dto as ratedto
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

api = TdxHq_API()

class stock_set_bid_price(object):

     #集合竞价大于多少手进入股票选取序列.
     def init_bid_price_stock(self,vol):
         listdata = []
         with api.connect(serviceinfo.HOST_IP, serviceinfo.HOST_PORT):
                 basicvos = basicvo.stock_infor_base_dto().get_basic_stock_infor()
                 for row in basicvos:
                     queryflag = False
                     market = 0
                     if str(row.code).startswith('0',0,1):
                         market = TDXParams.MARKET_SZ
                         queryflag = True
                     elif str(row.code).startswith('6',0,1):
                         market = TDXParams.MARKET_SH
                         queryflag = True
                     else:
                         continue

                     if(queryflag):
                         returndata = api.to_df(api.get_transaction_data(market,str(row.code), 0, 6000))
                         if(returndata.empty !=True):
                             try:
                                 data = returndata.sort_values(['time'], ascending=[True]).head(1)
                                 datas = list(data['vol'])[0]
                                 if(datas>vol):
                                   print(row.code + ':' + row.name)
                                   listdata.append(row)
                             except Exception as error:
                                 print('------->'+str(row.code) + ':' + str(row.name)+'----->执行查询出错')
         for row in listdata:
             print(str(row.code) + ':' + str(row.name)+'------->保存开始')
             vo = dto(code=row.code, name=row.name, industry=row.industry, createtime=datetime_utils.datetimeutils().get_current_time())
             dbmanager.sql_manager().single_common_save_basedata(vo)


     ##初始化集合竞价的值占流通股市值的比例
     def init_bid_price_stock_rate(self,vol,rate):
         listdata = []
         with api.connect(serviceinfo.HOST_IP, serviceinfo.HOST_PORT):
                 basicvos = basicvo.stock_infor_base_dto().get_basic_stock_infor()
                 for row in basicvos:
                     queryflag = False
                     market = 0
                     if str(row.code).startswith('0',0,1):
                         market = TDXParams.MARKET_SZ
                         queryflag = True
                     elif str(row.code).startswith('6',0,1):
                         market = TDXParams.MARKET_SH
                         queryflag = True
                     else:
                         continue

                     if(queryflag):
                         returndata = api.to_df(api.get_transaction_data(market,str(row.code), 0, 6000))
                         if(returndata.empty !=True):
                             try:
                                 data = returndata.sort_values(['time'], ascending=[True]).head(1)
                                 datas = list(data['vol'])[0]
                                 price = list(data['price'])[0]
                                 currentrate = float(datas*price*100/row.outstanding)
                                 #print(row.code + ':' + row.name+':'+str(currentrate)+':'+str(datas*price)+':'+str(row.outstanding))
                                 if datas>vol and currentrate>=rate:
                                   #pledgecount = pledge().get_stock_pledge_times(row.name)['average_value']
                                   print(row.code + ':' + row.name+':')
                                   listdata.append(row)
                             except Exception as error:
                                 continue
                                 #print('------->'+str(row.code) + ':' + str(row.name)+'----->执行查询出错')
         for row in listdata:
             currentdto = ratedto(code=row.code, name=row.name, industry=row.industry,
                                  createtime=datetime_utils.datetimeutils().get_current_time(), outstanding=row.outstanding)
             dbmanager.sql_manager().single_common_save_basedata(currentdto)

if __name__ == '__main__':
    #stock_set_bid_price().init_bid_price_stock_rate(500,0.0015)
    stock_set_bid_price().init_bid_price_stock(1000)