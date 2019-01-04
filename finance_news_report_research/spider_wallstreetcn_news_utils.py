# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import utils.spider_common_utils  as utils
import sys
import uuid

def daily_wallstreetcn_spider():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://wallstreetcn.com/live/a-stock")
    contents = driver.find_elements_by_class_name("live-item")
    for vo in contents:
        text = vo.find_element_by_class_name("live-item_html").text
        infor = utils.replace_special_character(text)
        index_date = vo.find_element_by_class_name("live-item_created").text
        href = vo.find_element_by_tag_name("a").get_attribute("href")
        print(index_date+":"+href)
        #print(vo.find_element_by_class_name("live-item_created").text)
        #print(vo.find_element_by_class_name("live-item_html").text)
        #print(vo.find_element_by_css_selector("div[class='live-item_created importance']"))





if __name__=='__main__':
    daily_wallstreetcn_spider()
