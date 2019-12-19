from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os


class NoProductFoundException(Exception):
    pass

def connectToWebSite(url, ignoreTerm=None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    driver = webdriver.Chrome(executable_path=dir_path + "\chromedriver.exe")
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
            name = processString(name_html.getText(), ignoreTerm)
            price = processString(price_html.getText(), ignoreTerm)
            listMobile.append((name, price))
        except Exception as e:
            print("Error: " + str(e))
    return listMobile

def processString(a: str, ignoreTerm):
    temp = a.lstrip()
    if ignoreTerm is not None:
        for term in ignoreTerm:
            temp = temp.replace(term, "")
    temp = temp.rstrip()
    return temp

def getAllPages(url, param, ignoreTerm=None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path.replace("\\", "/")
    os.chmod(dir_path + '/chromedriver.exe', 0o755)
    allResult = []
    for i in range(1, 100):
        full_url = url + param + str(i)
        try:
            allResult += connectToWebSite(full_url, ignoreTerm)
        except NoProductFoundException as e:
            break
    return allResult


