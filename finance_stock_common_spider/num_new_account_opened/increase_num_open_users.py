import requests
import pandas as pd
import json

BASE_URL = 'http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/weeklystockaccountsnew.ashx?isxml=true'

def get_raw_data():
    response = requests.get(BASE_URL)
    raw_date = json.loads(response.text)
    date = raw_date['X'].split(',')
    increment = list(map(float,raw_date['Y'][0].split(',')))
    return {'date': date, 'increment': increment}

def generate_ts(data_dict):
    ts = pd.Series(data_dict['increment'], index=pd.to_datetime(data_dict['date']))
    return ts

def get_account_increment():
    data = get_raw_data()
    return generate_ts(data)

if __name__ == '__main__':
    account_increment = get_account_increment()
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