# coding=utf-8
import jieba
from finance_news_report_analysis import spider_stock_notice_utils as spidernews
from finance_news_report_analysis import notice_constant as constant
from finance_stock_dao_model.stock_core_words_data_dto import  stock_core_words_data_dto as corewords
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from sqlalchemy.orm import scoped_session

class stock_news_research_utils(object):

      def __init__(self,spidernews):
          self.spidernews = spidernews

      def get_basic_core_words(self,weight):
        Session = scoped_session(dbmanager.sql_manager().open_session_factory())
        session = Session()
        data = session.query(corewords).filter(corewords.word_weight==weight).all()
        session.close()
        list = []
        for dto in data:
            print('基础数据:',dto.core_word)
            list.append(dto.core_word)
        return list

      def study_current_dict(self,weight,txt):
          ##读取本地的词根
          list = self.get_basic_core_words(weight)
          for word in list:
              jieba.add_word(word)
          ##分词基于当前词根产生的新的词义
          addlist=[]
          data = jieba.cut(txt)
          for mess in data:
              for messdata in list:
                  if mess.find(messdata) !=-1 and mess not in list:
                     if mess not in addlist:
                        addlist.append(mess)
                        print('学习到的新语言----->:'+mess)

          ##新的词义写入到当前的文档
          for adddata in addlist:
              vo = corewords(core_word=adddata,word_weight=weight)
              dbmanager.sql_manager().single_common_save_basedata(vo)


      def study_stock_notice_news(self,weight):
          obj = stock_news_research_utils(self.spidernews)
          for newsreport in self.spidernews:
              obj.study_current_dict(weight,newsreport.info_title)


      def select_current_news_stock(self,newsflag):
          ##读取本地的词根
          list = self.get_basic_core_words(newsflag)
          ##获取所有的有利消息标志.
          obj = stock_news_research_utils(self.spidernews)
          for newsreport in self.spidernews:
              infotitle = newsreport.info_title
              newsreport.news_flag = newsflag
              forflag = False
              for goodflag in list:
                  if infotitle.find(goodflag) != -1:
                     forflag = True
                     break
              if(forflag):
                  dbmanager.sql_manager().single_common_save_basedata(newsreport)



if __name__ == '__main__':
     spidernotices = spidernews.exchange_stock_notice_manager().get_announcement_all_notice()
     constantdict = constant.notice_constant()
     stock_news_research_utils(spidernotices).study_stock_notice_news(constantdict.GOOD_NEWS_FLAG)
     stock_news_research_utils(spidernotices).select_current_news_stock(constantdict.GOOD_NEWS_FLAG)