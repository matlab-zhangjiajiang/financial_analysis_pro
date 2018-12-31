# coding=utf-8
import tushare as tu
import pandas as pd

#http://finance.sina.com.cn/7x24/


import requests
import time
from bs4 import BeautifulSoup

def sina():
    is_first = True
    task_q = [] # 本地存储新闻
    task_time = []
    while True:
        data_list = getNews()

        if is_first:
            task_q = data_list
            for data in data_list:
                print(data['n_time'],data['n_info'])
                time.sleep(0.5)
                task_time.append(data['n_time'])
            is_first = False
        else:
            for data in data_list:
                if data['n_time'] in task_time:
                    pass
                else:
                    task_time.append(data['n_time'])
                    print('-'*30)
                    print('新消息',data['n_time'],data['n_info'])

        time.sleep(5)

def getNews(): # 获取新闻函数
    news_list =[]
    base_url = 'http://live.sina.com.cn/zt/f/v/finance/globalnews1'
    response = requests.get(base_url)
    response.encoding = response.apparent_encoding
    html = response.text

    html_bs4 = BeautifulSoup(html,'lxml')
    info_list = (html_bs4.find_all('div',{'data-nick':'fin_图文直播'}))

    for info in info_list:  # 获取页面中自动刷新的新闻
        n_time = info.select('p[class="bd_i_time_c"]')[0].get_text()  # 新闻时间及内容
        n_info = info.select('p[class="bd_i_txt_c"]')[0].get_text()
        data = {
            'n_time': n_time,
            'n_info': n_info
        }
        news_list.append(data)
    return news_list[::-1] # 这里倒序，这样打印时才会先打印旧新闻，后打印新新闻

if __name__ == '__main__':
    sina()