#utf-8
import requests
import pandas as pd
import json

BASE_URL = 'http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/weeklystockaccountsnew.ashx?isxml=true'

class increase_num_open_users(object):

   def get_raw_data(self):
       response = requests.get(BASE_URL)
       raw_date = json.loads(response.text)
       print(raw_date)
       date = raw_date['X'].split(',')
       increment = list(map(float,raw_date['Y'][0].split(',')))
       return {'date': date, 'increment': increment}

   def generate_ts(self,data_dict):
       ts = pd.Series(data_dict['increment'], index=pd.to_datetime(data_dict['date']))
       return ts

   def get_account_increment(self):
       data = self.get_raw_data()
       return self.generate_ts(data)

if __name__ == '__main__':
    account_increment =increase_num_open_users().get_account_increment()
    # ��ӡ��������
    print(account_increment)
    # �����׼��
    print(account_increment.std())
    # ������Сֵ
    print(account_increment.min())
    # �������ֵ
    print(account_increment.max())
    # �����ֵ
    print(account_increment.mean())