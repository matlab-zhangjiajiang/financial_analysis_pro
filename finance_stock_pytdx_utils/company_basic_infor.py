#coding=utf-8
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
from connection_host_server import connection_host_server as serviceinfo
api = TdxHq_API()

def get_company_basic_infor():
    with api.connect(serviceinfo.HOST_IP, serviceinfo.HOST_PORT):
      df = api.get_and_parse_block_info(TDXParams.BLOCK_SZ)

      print(df)





if __name__ == '__main__':
    get_company_basic_infor()