from ScrapEngine import ScrapEngine
from PhoneData import PhoneData

import DatabaseEngine

DatabaseEngine.createTable()

"""
url = "https://hoanghamobile.com/dien-thoai-di-dong-c14.html"
param = "?sort=0&p="
ignoreTerm = ["Chính hãng", "Chính Hãng", "-"]
scraper = ScrapEngine()
result = scraper.getAllPages(url, param, ignoreTerm)
data = []
for item in result:
    try:
        data.append(PhoneData(name=item[0], price_str=item[1]))
    except:
        print("Unable to parse: " + item[0] + ": " + item[1])

print("done")
"""