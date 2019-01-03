#coding=utf-8
from pytdx.hq import TdxHq_API
import pandas as pd
from pytdx.crawler.history_financial_crawler import HistoryFinancialListCrawler
from pytdx.crawler.history_financial_crawler import HistoryFinancialCrawler
from pytdx.reader.history_financial_reader import HistoryFinancialReader
from pytdx.crawler.base_crawler import demo_reporthook
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from system_stock_financial_analysis import get_financial_rename_list_utils as renames
import os

#系统属性设置.
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
api = TdxHq_API()
pd.set_option('display.max_columns',None,'precision',5)


class get_financial_infor_utils(object):



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


      #按季度查询当前所有的财报数据
      def get_current_time_finance_research_report(self,time):
          filename = 'gpcw'+time+'.zip'
          data = self.get_single_financial_resource(filename)

          return data.sort_values(['numberOfShareholders'],ascending=[True]).head(200)


      #保存所有的pandas基础信息.
      def save_current_data_information(self,all_data_pandas):
          engine = dbmanager.sql_manager().init_engine()
          pd.io.sql.to_sql(all_data_pandas, 'finance_system_stock_financial_analysis_data', con=engine,
                           if_exists='replace', index=False, chunksize=1000)


      def get_current_target(self,code,columnlist):
          dowllist = self.get_all_financial_list_utils()
          downroad = list(dowllist['filename'])
          all_data_pandas = None
          i=0
          for name in downroad:
              data = self.get_single_financial_resource(name)
              currentdate = name[4:len(name)-4]
              filterdata = data.loc[data.index==code,columnlist].drop_duplicates()
              if (filterdata.empty != True):
                  #filterdata['date'] = currentdate
                  filterdata.index = [currentdate]
                  filterdata['year'] = [currentdate]
                  if (i == 0):
                      all_data_pandas = filterdata
                  else:
                      all_data_pandas = pd.concat([all_data_pandas, filterdata])
              i +=1
          self.save_current_data_information(all_data_pandas)



if __name__ == '__main__':
     #obj = get_financial_infor_utils()
     #data = obj.get_current_time_finance_research_report('20180930')
     #obj.save_current_data_information(data)
     #print(data)

     #all_financial_infor_utils().get_single_financial_resource('gpcw20180930.zip')

     code = '600781'
     columnlist= ['EPS','ROE','turnoverRatioOfInventory','currentRatio','numberOfShareholders','accountsReceivables','daysSalesOutstanding','cashRatio',
                  'goodwill','netProfit']
     get_financial_infor_utils().get_current_target(code,columnlist)