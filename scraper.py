from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os


class NoProductFoundException(Exception):
    pass


def connectToWebSite(url):
    driver = webdriver.Chrome(executable_path="C:/Users/10058205/Documents/WebScraper/chromedriver.exe")
    driver.get(url)
    content = driver.page_source
    driver.close()
    soup = BeautifulSoup(content, features="html.parser")
    listMobile = []
    listProduct = soup.find('div', attrs={'class':'product-list'})
    allProducts = listProduct.findAll('div', attrs={'class': 'list-item'})
    if len(allProducts) == 0:
        raise NoProductFoundException
    for a in allProducts:
        name_html = a.find('div', attrs={'class': 'product-name'})
        price_html = a.find('div', attrs={'class': 'product-price'})
        try:
            name = processString(name_html.getText())
            price = processString(price_html.getText())
            listMobile.append((name, price))
        except Exception as e:
            print("Error: " + str(e))
    return listMobile

def processString(a: str):
    temp = a.lstrip()
    temp = temp.replace("Chính hãng", "")
    temp = temp.replace("-", "")
    temp = temp.rstrip()
    return temp

def getAllPages(url, param):
    os.chmod('C:/Users/10058205/Documents/WebScraper/chromedriver', 0o755)
    allResult = []
    for i in range(1, 100):
        full_url = url + param + str(i)
        try:
            allResult += connectToWebSite(full_url)
        except NoProductFoundException as e:
            break
    return allResult


url = "https://hoanghamobile.com/dien-thoai-di-dong-c14.html"
param = "?sort=0&p="

result = getAllPages(url, param)
for item in result:
    print(str(item[0]) + ": " + str(item[1]))
