#coding=utf-8
from datetime import datetime
import time
import calendar

class datetimeutils(object):

    def __init__(self):
        print('初始化时间工具类')

    def get_current_time(self):
        return datetime.now().strftime('%Y-%m-%d')

    def get_current_time_new(self):
        return datetime.now().strftime('%Y%m%d')

    def get_current_datetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ###获取当前时间所在的季度.
    def get_current_month_quarter(self):
        Qnum = 0
        currentmonth = datetime.now().strftime('%Y-%m').split('-')[1]
        if currentmonth in ['01','02','03']:
           Qnum =1
        elif currentmonth in ['04','05','06']:
           Qnum =2
        elif currentmonth in ['07','08','09']:
           Qnum =3
        else:
           Qnum =4
        return Qnum

    def check_current_data_or_workday(self):
        date = datetime.now().isoweekday()
        if date in [1,2,3,4,5]:
            return True
        else: return False

if __name__ == '__main__':
    print(datetimeutils().get_current_time_new())