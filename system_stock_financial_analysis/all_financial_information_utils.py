#coding=utf-8
from pytdx.hq import TdxHq_API
import pandas as pd
from pytdx.params import TDXParams
from finance_stock_pytdx_utils.connection_host_server import connection_host_server as serviceinfo
from pytdx.crawler.history_financial_crawler import HistoryFinancialListCrawler
from pytdx.crawler.history_financial_crawler import HistoryFinancialCrawler
from pytdx.reader import HistoryFinancialReader
from pytdx.crawler.base_crawler import demo_reporthook
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_stock_pytdx_utils import rename_list_utils as renames
import os

#系统属性设置.
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
api = TdxHq_API()
pd.set_option('display.max_columns',None,'precision',5)


class all_financial_infor_utils(object):

      def get_all_financial_list_utils(self):
          crawler = HistoryFinancialListCrawler()
          list_data = crawler.fetch_and_parse()
          return pd.DataFrame(data=list_data)


      def get_all_financial_resource(self):
          dowllist = self.get_all_financial_list_utils()
          downroad = list(dowllist['filename'])
          datacrawler = HistoryFinancialCrawler()
          for road in downroad:
              datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename=road,path_to_download=road)

      def get_single_financial_resource(self,current_filename):
          datacrawler = HistoryFinancialCrawler()
          if os.path.exists(current_filename) != True:
             currentdata = datacrawler.fetch_and_parse(reporthook=demo_reporthook,filename=current_filename,path_to_download=current_filename)
          reader = HistoryFinancialReader()
          database_data = reader.get_df(current_filename)
          database_data = renames.rename_list_utils().rename_current_finance_utils(database_data)
          print(database_data)
          database_data.to_excel('currentdata.xlsx')


if __name__ == '__main__':
     all_financial_infor_utils().get_single_financial_resource('gpcw20180930.zip')