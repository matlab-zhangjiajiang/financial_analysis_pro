# coding=utf-8

from datetime import datetime
from finance_stock_dao_model.exchange_stock_notice_infor_dto import exchange_stock_notice_infor_dto as dto

NEWS_PLATFORM = {'sse.com': 'SSE'}
NEWS_URL={'sse.com':'http://www.sse.com.cn/disclosure/listedinfo/announcement/'}


class exchange_stock_notice_manager(object):

    # 获取当前交易所网站上显示的所有上市公司公告
    # @update: 8.29
    # @return: 当前交易所网站上显示的所有上市公司公告信息
    def get_announcement_all(self):
        print('----main----')
        # splits = s.split(',')                           # 切割公告信息
        # info_code = splits[0].strip('[').strip('"')     # 分离股票代码
        # info_url = targeturl+splits[1].strip('"')                 # 分离URL链接地址
        # info_title = splits[2].strip('"')               # 公告标题
        # info_time = splits[-1].strip('"').strip(']')    # 公告时间戳
        # key_time = info_time[0:10]                      # 公告时间
        # vo = dto(stock_code=info_code,info_url=info_url,info_title=info_title,key_time=key_time)
        # infordata.append(vo)
        # return infordata

if __name__ == '__main__':
    exchange_stock_notice_manager().get_announcement_all()