from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import uuid

def dailyCnfolBlogSpider(link):

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(link)
    resultList = driver.find_elements_by_class_name('ArticleBox')
    listArray = []
    count = 1
    for div in  resultList:
        descriptContext = div.find_element_by_class_name('strContent').text
        titleHtml = div.find_element_by_tag_name('h2').find_element_by_tag_name('a')
        title = titleHtml.text
        linkUrl = titleHtml.get_attribute('href')
        count +=1
        listArray.append([id,title,linkUrl,''])
    return listArray



def writeDailyCnfolBlogSpider():
    linkUrl = 'http://new.blog.cnfol.com/zhangping626'
    print(dailyCnfolBlogSpider(linkUrl))


if __name__=='__main__':
    writeDailyCnfolBlogSpider()
