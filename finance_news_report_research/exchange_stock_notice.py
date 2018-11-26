# coding=utf-8

from datetime import datetime
import urllib2
import urllib
import codecs
import re
from finance_stock_dao_model.exchange_stock_notice_infor_dto import exchange_stock_notice_infor_dto as dto
import finance_common_utils.mysql_dbutils.sqlalchemy_dbutils as dbmanager

###https://www.lfd.uci.edu/~gohlke/pythonlibs/
###http://quant.10jqka.com.cn/platform/html/article.html#id/89446584


class exchange_stock_notice_manager(object):

    # 打开文件
    def open_file(self,path):
        return codecs.open(path, 'w', encoding='utf-8')

    # 写入文件
    def write(self,f, line):
        f.write(line+'\n')

    # 关闭文件
    def close_file(self,f):
        f.close()

    #访问目标URL
    def request2url(self,url, header, data):
        request = urllib2.Request(url, headers=header, data=data)
        response = urllib2.urlopen(request)
        return response.read()

    # 获取当前交易所网站上显示的所有上市公司公告
    # @update: 8.29
    # @return: 当前交易所网站上显示的所有上市公司公告信息
    def get_announcement_all(self):
        today = datetime.now().strftime('%Y%m%d%H%M')   # 当前日期时间
        url = 'http://disclosure.szse.cn//disclosure/fulltext/plate/szlatest_24h.js?ver='+today     # 访问目标URL
        headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'keep-alive',
               'Host': 'disclosure.szse.cn',
               'Referer': 'http://disclosure.szse.cn/m/unit/drggxxpllist.html? \
                          s=%2Fdisclosure%2Ffulltext%2Fplate%2Fszlatest_24h.js'}    # 生成访问头
        data = urllib.urlencode({'ver': today})             # 生成访问数据
        result = self.request2url(url, headers, data)            # 请求目标网页
        result = result.decode('gbk')                       # 转换编码
        pattern = re.compile(ur'\[(.*?)\]')                 # 匹配每条公告
        pattern_result = pattern.findall(result)            # 匹配结果
        #f = self.open_file('announcement_' + today + '.dat')      # 新建文件
        for s in pattern_result:
            splits = s.split(',')                           # 切割公告信息
            info_code = splits[0].strip('[').strip('"')     # 分离股票代码
            info_url = splits[1].strip('"')                 # 分离URL链接地址
            info_title = splits[2].strip('"')               # 公告标题
            info_time = splits[-1].strip('"').strip(']')    # 公告时间戳
            key_time = info_time[0:10]                      # 公告时间
            vo = dto(stock_code=info_code,info_url=info_url,info_title=info_title,key_time=key_time)
            dbmanager.sql_manager().single_common_save_basedata(vo)
            #line = info_code+' '+info_url+' '+info_title+' '+key_time   # 拼接一条公告
            #self.write(f, line)                                  # 写入文件
        #self.close_file(f)


if __name__ == '__main__':
    exchange_stock_notice_manager().get_announcement_all()