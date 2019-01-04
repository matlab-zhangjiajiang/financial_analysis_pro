# coding=utf-8
import tushare as tu
import pandas as pd

#http://finance.sina.com.cn/7x24/


import requests
import time
from bs4 import BeautifulSoup


import requests
from bs4 import BeautifulSoup
res = requests.get('http://news.sina.com.cn/china/')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text,'html.parser')
print(soup)
for news in soup.select('.news-item'):
    print(news)
    if len(news.select('h2')) >0 :
       time = news.select('.time')[0].text
       h2 = news.select('h2')[0].text
       a =  news.select('a')[0]['href']
       print(time,h2,a)