#coding=utf-8
import os

class notice_research_constant(object):

      def get_bad_dict_path(self):
          project_path = os.path.dirname(os.path.realpath(__file__))  # 获取项目路径
          baddict_address = '\\bad_dict.txt'
          return project_path+baddict_address

      def get_good_dict_path(self):
            project_path = os.path.dirname(os.path.realpath(__file__))  # 获取项目路径
            gooddict_address = '\\good_dict.txt'
            return project_path + gooddict_address

      GOOD_NEWS_FLAG = 1

      BAD_NEWS_FLAG = 0

      NEWS_PLATFORM={'wallstreetcn':'WALLSTREETCN'}

if __name__ == '__main__':
    notice_research_constant().get_bad_dict_path()
