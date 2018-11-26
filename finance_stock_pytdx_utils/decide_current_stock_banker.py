#coding=utf-8
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
from finance_stock_dao_model import stock_infor_base_dto as basicvo
from connection_host_server import connection_host_server as serviceinfo
from finance_common_utils.common_utils.datetime_model import datetime_utils
import finance_common_utils.mysql_dbutils.sqlalchemy_dbutils as dbmanager
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

api = TdxHq_API()


class decide_current_stock_banker(object):


    def decide_stock_banker(self):
        listdata = []
        with api.connect(serviceinfo.HOST_IP, serviceinfo.HOST_PORT):
            basicvos = basicvo.stock_infor_base_dto().get_basic_stock_infor()
            for row in basicvos:
                queryflag = False
                market = 0
                if str(row.code).startswith('0', 0, 1):
                    market = TDXParams.MARKET_SZ
                    queryflag = True
                elif str(row.code).startswith('6', 0, 1):
                    market = TDXParams.MARKET_SH
                    queryflag = True
                else:
                    continue

                if (queryflag):
                    returndata = api.to_df(api.get_transaction_data(market, str(row.code), 0, 6000))
                    if (returndata.empty != True):
                        try:
                            data = returndata.sort_values(['time'], ascending=[True])
                            print(data)
                            datas = list(data['vol'])[0]
                        except Exception as error:
                            print('------->' + str(row.code) + ':' + str(row.name) + '----->执行查询出错')

if __name__ == '__main__':
    decide_current_stock_banker().decide_stock_banker()
    #returndata = api.to_df(api.get_transaction_data(TDXParams.MARKET_SZ,'000006', 0, 1600))
    #print(returndata)