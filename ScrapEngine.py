from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options
import os


class NoProductFoundException(Exception):
    pass

class ScrapEngine:

    def connectToWebSite(self, url, ignoreTerm=None):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        options = Options()
        options.add_argument("--no-sandbox");
        options.add_argument("--headless");
        options.add_argument("disable-gpu");
        options.add_argument("--disable-dev-shm-usage");
        driver = webdriver.Chrome(options=options)
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
            name_html = self.hideInvalidTag(a.find('div', attrs={'class': 'product-name'}), ['strike'])
            price_html = self.hideInvalidTag(a.find('div', attrs={'class': 'product-price'}), ['strike'])
            try:
                name = self.processString(name_html.getText(), ignoreTerm)
                price = self.processString(price_html.getText(), ignoreTerm)
                href = "n.a"
                try:
                    temp = name_html.find('a', href=True)
                    href = urljoin(url, temp['href'])
                except Exception as e:
                    pass
                listMobile.append((name, price, href))
            except Exception as e:
                print("Error: " + str(e))
        print("Done with: " + url)
        return listMobile

    def processString(self, a: str, ignoreTerm):
        temp = a.lstrip()
        if ignoreTerm is not None:
            for term in ignoreTerm:
                temp = temp.replace(term, "")
        temp = temp.rstrip()
        return temp

    def getAllPages(self, url, param, ignoreTerm=None):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path.replace("\\", "/")
        os.chmod(dir_path + '/chromedriver.exe', 0o755)
        allResult = []
        for i in range(1, 100):
            full_url = url + param + str(i)
            try:
                allResult += self.connectToWebSite(full_url, ignoreTerm)
            except NoProductFoundException as e:
                break
        return allResult

    def hideInvalidTag(self, originalContent, invalidTag:[str]):
        for tag in invalidTag:
            [x.extract() for x in originalContent.findAll(tag)]
        return originalContent
