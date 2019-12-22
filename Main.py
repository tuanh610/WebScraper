from ScrapEngine import ScrapEngine
from PhoneData import PhoneData

import DatabaseEngine
from DatabaseEngine import dynammoDBAdapter



url = "https://hoanghamobile.com/dien-thoai-di-dong-c14.html"
param = "?sort=0&p="

ignoreTerm = ["Chính hãng", "Chính Hãng", "-"]
scraper = ScrapEngine()
result = scraper.getAllPages(url, param, ignoreTerm)
#result = scraper.connectToWebSite(url, ignoreTerm)
data = []
for item in result:
    try:
        data.append(PhoneData(name=item[0], price=item[1], info={"url": item[2]}))
    except:
        print("Unable to parse: " + item[0] + ": " + item[1])

#Database Update
DatabaseEngine.createTable("PriceList")
dbEngine = dynammoDBAdapter("PriceList")
dataFromDB = dbEngine.getAllDataFromTable()

updateNeeded = []
newItem = []
#compare data
for item in data:
    existed = False
    for phone in dataFromDB:
        if item.getName() == phone.getName():
            if item.getPrice() != phone.getPrice() or item.getInfo() != phone.getInfo():
                updateNeeded.append(item)
            existed = True
            break
    if not existed:
        newItem.append(item)

for item in updateNeeded:
    dbEngine.updateItemToDB(item)
dbEngine.pushAllDataToDB(newItem)
#update item
print("done")