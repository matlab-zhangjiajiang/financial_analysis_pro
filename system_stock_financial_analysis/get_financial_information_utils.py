#coding=utf-8
from pytdx.hq import TdxHq_API
import pandas as pd
import threadpool as tp
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


class get_financial_infor_utils(object):

      returnfilterdata =[]

      def __init__(self,code,columnlist):
          self.code = code
          self.columnlist = columnlist


      def get_all_financial_list_utils(self):
          crawler = HistoryFinancialListCrawler()
          list_data = crawler.fetch_and_parse()
          return pd.DataFrame(data=list_data)



      def get_all_financial_resource(self):
          dowllist = self.get_all_financial_list_utils()
          downroad = list(dowllist['filename'])
          datacrawler = HistoryFinancialCrawler()
          for road in downroad:
              if os.path.exists(road) != True:
                 datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename=road,path_to_download=road)


      def get_single_financial_resource(self,current_filename):
          datacrawler = HistoryFinancialCrawler()
          if os.path.exists(current_filename) != True:
             currentdata = datacrawler.fetch_and_parse(reporthook=demo_reporthook,filename=current_filename,path_to_download=current_filename)
          reader = HistoryFinancialReader()
          database_data = reader.get_df(current_filename)
          database_data = renames.rename_list_utils().rename_current_finance_utils(database_data)
          return database_data


      def get_current_target_by_thread_fun(self,name):
          data = self.get_single_financial_resource(name)
          currentdate = name[4:len(name) - 4]
          filterdata = data.loc[data.index == self.code, self.columnlist].drop_duplicates()
          if (filterdata.empty != True):
              # filterdata['date'] = currentdate
              filterdata.index = [currentdate]
              filterdata['year'] = [currentdate]
              print(filterdata)


      def get_current_target_by_thread(self):
          dowllist = self.get_all_financial_list_utils()
          downroad = list(dowllist['filename'])
          pool = tp.ThreadPool(30)
          requests = tp.makeRequests(self.get_current_target_by_thread_fun, downroad)
          [pool.putRequest(req) for req in requests]
          pool.wait()


      def get_current_target(self):
          dowllist = self.get_all_financial_list_utils()
          downroad = list(dowllist['filename'])
          engine = dbmanager.sql_manager().init_engine()
          all_data_pandas = None
          i=0
          for name in downroad:
              data = self.get_single_financial_resource(name)
              currentdate = name[4:len(name)-4]
              filterdata = data.loc[data.index==self.code,self.columnlist].drop_duplicates()
              if (filterdata.empty != True):
                  #filterdata['date'] = currentdate
                  filterdata.index = [currentdate]
                  filterdata['year'] = [currentdate]
                  if (i == 0):
                      all_data_pandas = filterdata
                  else:
                      all_data_pandas = pd.concat([all_data_pandas, filterdata])
              i +=1
          print(all_data_pandas)
          pd.io.sql.to_sql(all_data_pandas, 'finance_system_stock_financial_analysis_data', con=engine,
                           if_exists='replace', index=False, chunksize=1000)


if __name__ == '__main__':
     #all_financial_infor_utils().get_all_financial_resource()
     #all_financial_infor_utils().get_single_financial_resource('gpcw20180930.zip')
     code = '001696'
     columnlist= ['EPS','ROE','turnoverRatioOfInventory','currentRatio','numberOfShareholders','daysSalesOfInventory']
     get_financial_infor_utils(code,columnlist).get_current_target()