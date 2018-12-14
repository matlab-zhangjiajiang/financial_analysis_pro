# coding=utf-8
import jieba
import sys
from finance_stock_dao_model.exchange_stock_notice_infor_dto import exchange_stock_notice_infor_dto as dto
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_news_report_research import exchange_stock_notice as spidernews
reload(sys)
sys.setdefaultencoding('utf-8') #设置系统运行编码

url="E:\\GitHub\\financial_analysis_pro\\finance_news_report_research\\good_dict.txt"

class stock_news_research_utils(object):


      def __init__(self,spidernews):
          self.spidernews = spidernews

      def study_current_dict(self,txt):

          ##读取本地的词根
          list =[]
          file = open(url,'r')
          for line in file:
              linedata = line.replace('\n','')
              list.append(linedata)
          file.close()

          ##分词基于当前词根产生的新的词义
          jieba.load_userdict(url)
          addlist=[]
          data = jieba.cut(txt)
          for mess in data:
              for messdata in list:
                  if mess.find(messdata) !=-1 and mess not in list:
                     if mess not in addlist:
                        addlist.append(mess)
                        print('学习到的新语言----->:'+mess)

          ##新的词义写入到当前的文档
          writefile = open(url, 'a')
          for adddata in addlist:
              writefile.write('\n'+adddata)


      def study_stock_notice_news(self):
          obj = stock_news_research_utils(self.spidernews)
          for newsreport in self.spidernews:
              obj.study_current_dict(newsreport.info_title)


      def select_good_news_stock(self):
          ##读取本地的词根
          list = []
          file = open(url, 'r')
          for line in file:
              linedata = line.replace('\n', '')
              list.append(linedata)
          file.close()

          ##获取所有的有利消息标志.
          obj = stock_news_research_utils(self.spidernews)
          for newsreport in self.spidernews:
              infotitle = newsreport.info_title
              forflag = False
              for goodflag in list:
                  if infotitle.find(goodflag) != -1:
                     forflag = True
                     break
              if(forflag):
                  dbmanager.sql_manager().single_common_save_basedata(newsreport)


if __name__ == '__main__':
    spidernotices = spidernews.exchange_stock_notice_manager().get_announcement_all()
    stock_news_research_utils(spidernotices).study_stock_notice_news()
    stock_news_research_utils(spidernotices).select_good_news_stock()