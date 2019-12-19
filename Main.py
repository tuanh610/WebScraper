import ScrapEngine


url = "https://hoanghamobile.com/dien-thoai-di-dong-c14.html"
param = "?sort=0&p="
ignoreTerm = ["Chính hãng", "Chính Hãng", "-"]
scraper = ScrapEngine()
result = scraper.getAllPages(url, param, ignoreTerm)
for item in result:
    print(str(item[0]) + ": " + str(item[1]))

