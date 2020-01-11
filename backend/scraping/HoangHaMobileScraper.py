import os.path
import backend.scraping.ScrapEngine as ScrapEngine

from urllib.parse import urljoin

class NoProductFoundException(Exception):
    pass

class HoangHaMobileScraper:
    def __init__(self, ignoreTerm, url, param):
        self.url = url
        self.ignoreTerm = ignoreTerm
        self.param = param

    def parseData(self, content, url):
        listMobile = []
        listProduct = content.find('div', attrs={'class': 'product-list'})
        allProducts = listProduct.findAll('div', attrs={'class': 'list-item'})
        if len(allProducts) == 0:
            raise NoProductFoundException
        for a in allProducts:
            image_html = ScrapEngine.hideInvalidTag(a.find('img'), ['strike'])
            name_html = ScrapEngine.hideInvalidTag(a.find('div', attrs={'class': 'product-name'}), ['strike'])
            price_html = ScrapEngine.hideInvalidTag(a.find('div', attrs={'class': 'product-price'}), ['strike'])
            try:
                image_src = image_html['src']
                name = ScrapEngine.processString(name_html.getText(), self.ignoreTerm)
                price = ScrapEngine.processString(price_html.getText(), self.ignoreTerm)
                href = "n.a"
                try:
                    temp = name_html.find('a', href=True)
                    href = urljoin(url, temp['href'])
                except Exception as e:
                    pass
                listMobile.append((name, price, href, image_src))
            except Exception as e:
                print("Error: " + str(e))
        print("Done with: " + url)
        return listMobile

    def getOnePage(self, URL):
        return self.parseData(ScrapEngine.connectToWebSite(URL, self.ignoreTerm), URL)

    def getAllPages(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path.replace("\\", "/")
        allResult = []
        for i in range(1, 100):
            full_url = self.url + self.param + str(i)
            try:
                allResult += self.getOnePage(full_url)
            except NoProductFoundException as e:
                break
        return allResult
