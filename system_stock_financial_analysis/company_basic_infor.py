#coding=utf-8
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
from finance_stock_pytdx_utils.connection_host_server import connection_host_server as serviceinfo
from finance_common_utils.common_utils import loggger_factory as loggers


api = TdxHq_API()

logger = loggers.Logger(logname='log.txt', loglevel=1, logger="company_basic_infor").getlog()

def get_company_basic_infor():
    with api.connect(serviceinfo.HOST_IP, serviceinfo.HOST_PORT):
      datas = api.get_finance_info(0, '000001')
      logger.info(datas)






if __name__ == '__main__':
    get_company_basic_infor()