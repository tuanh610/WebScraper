import unittest
from unittest.mock import patch
from ScrapEngine import ScrapEngine
from bs4 import BeautifulSoup
import os

class TestScrapEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = ScrapEngine()

    def test_connecttoWebsite(self):
        url = os.path.dirname(os.path.realpath(__file__)) + "/../testdata/testWebsite.html"
        ignoreTerm = ["Chính hãng", "Chính Hãng", "-"]
        result = self.scraper.connectToWebSite(url, ignoreTerm)
        self.assertEqual(20, len(result))
        self.assertEqual(result[0][0], "Samsung Galaxy A50  6GB/128GB")
        self.assertEqual(result[0][1], "5.550.000 ₫")
        self.assertEqual(result[0][2], "https://hoanghamobile.com/samsung-galaxy-a50-6gb128gb-chinh-hang-p14862.html")

    def test_processString(self):
        test = "     hello world 213 #$%@*^)@    "
        ignore = ["!", "@", "#", "$", "%", "^", "&", "*", ")", "("]
        output = "hello world 213"
        self.assertEqual(output, self.scraper.processString(test, ignore))

    def test_hideTag(self):
        tag = ['a', 'li', 'strike']
        url = os.path.dirname(os.path.realpath(__file__)) + "/../testdata/testWebsite.html"
        content = open(url, encoding='utf8')
        soup = BeautifulSoup(content.read(), features="html.parser")
        result = self.scraper.hideInvalidTag(soup, tag)
        temp1 = result.findAll('a')
        temp2 = result.findAll('li')
        temp3 = result.findAll('div')
        self.assertEqual(0, len(temp1))
        self.assertEqual(0, len(temp2))
        self.assertNotEqual(0, len(temp3))

        temp = "<div class=\"product-price\"><strike>33.990.000 ₫</strike> 29.890.000 ₫</div>"
        soup = BeautifulSoup(temp, features="html.parser")
        temp1 = soup.findAll('strike')
        self.assertEqual(1, len(temp1))
        result = self.scraper.hideInvalidTag(soup, tag)
        temp1 = result.findAll('strike')
        self.assertEqual(0, len(temp1))

if __name__ == '__main__':
    unittest.main()
