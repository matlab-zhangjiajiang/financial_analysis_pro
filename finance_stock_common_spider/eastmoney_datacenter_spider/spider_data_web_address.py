#coding=utf-8

class spider_web_address(object):

      DATA_URL = {'INCREASE_USERS':'http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/weeklystockaccountsnew.ashx?isxml=true',
                  'DAYLY_INCREASE_HOLDINGS': 'http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/GDZC/GetGDZC?tkn=eastmoney&cfg=gdzc&secucode=&fx=1&sharehdname=&pageSize=50&pageNum=1&sortFields=NOTICEDATE&sortDirec=1&startDate=&endDate=',
                  'TOP_TEN_CIRCULATE_HOLDER':'http://emweb.securities.eastmoney.com/ShareholderResearch/Index?type=web&code=',
                  'TOP_TEN_HOLDER_ADDER':'http://data.eastmoney.com/DataCenter_V3/gdfx/data.ashx?SortType=NDATE&SortRule=1&PageIndex=1&PageSize=100&jsObj=DlswLagO&type=NSHDDETAIL&date=&gdlx=0&cgbd=1&rt=52888792'}