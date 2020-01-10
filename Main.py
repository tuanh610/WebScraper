from backend.ScrapEngine import ScrapEngine
from backend.PhoneData import PhoneData
from backend.SourceData import SourceData
from backend.mailingModule import mailModule
from backend import DatabaseEngine
from backend.DatabaseEngine import dynammoDBAdapter, DynamoElement
import backend.constant as constant

notifyByEmail = False


#Get source data
DatabaseEngine.createTable(constant.sourceTableName, constant.sourceElements)
sourceDB = dynammoDBAdapter(constant.sourceTableName)
sourceData = sourceDB.getAllDataFromTable()

DatabaseEngine.createTable("PriceList")
dbEngine = dynammoDBAdapter("PriceList")
dataFromDB = dbEngine.getAllDataFromTable()
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
#Update data
for item in data:
    existed = False
    for phone in dataFromDB:
        if item.getName() == phone.getName():
            if item.getPrice() != phone.getPrice() or item.getInfo() != phone.getInfo():
                updateNeeded.append((item, phone))
            existed = True
            break
    if not existed:
        newItem.append(item)

#push new data to database
for item, _ in updateNeeded:
    dbEngine.updateItemToDB(item)

if len(newItem) > 0:
    dbEngine.pushAllDataToDB(newItem)

#send notification to user
"""
NotifyByEmail is false as I do not include the credentials and tokens of my Gmail account here 
Once the project is pulled from the projects, please use the link in mailingModule to get your
credentials.json file. Then enable this code by set notifyByEmail to true
"""
if notifyByEmail:
    content = ""
    if len(newItem) > 0:
        content += "New Items:\n"
        for item in newItem:
            info = item.getInfo()
            content += "Name: %s. Price: %d %s\n" %(item.getName(), item.getPrice(), info["currency"])
            if "url" in info:
                content += "URL: %s\n" % info["url"]
    if len(updateNeeded) > 0:
        content += "Price Change Items:\n"
        for item, oldItem in updateNeeded:
            info = item.getInfo()
            oldInfo = oldItem.getInfo()
            content += "Name: %s. Old price: %d %s. New Price: %d %s\n" %(item.getName(),
                                                                        oldItem.getPrice(),
                                                                        oldInfo["currency"],
                                                                        item.getPrice(), info["currency"])
    if content == "":
        content = "No update needed"

    mail = mailModule()
    service = mail.getCredential()
    message = mail.create_message("warmboy610@gmail.com", "tuanh.dang610@gmail.com", "Update Price", content)
    result = mail.send_message(service, message)
    print(result)

#update item
print("done")