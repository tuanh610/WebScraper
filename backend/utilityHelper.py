import backend.scraping.PhoneData as PhoneData
import backend.database.phoneDBEngine as phoneDBEngine
import backend.constant as constant

@staticmethod
def arrangePhonesToList(phones: [PhoneData]):
    data = {}
    for phone in phones:
        if phone.getName() in data:
            data[phone.getName()].append(phone)
        else:
            data[phone.getName()] = [phone]
    return data

@staticmethod
def getLowestPriceList(phones: [PhoneData]):
    data = {}
    for phone in phones:
        if phone.getName() not in data or phone.getPrice() < data[phone.getName()].getPrice():
            data[phone.getName()] = phone
    return data

@staticmethod
def initBrandsUsingTextFile():
    phoneDBAdaper = phoneDBEngine(constant.dynamoDBTableName)
    f = open("brands.txt", "r")
    content = f.read()
    f.close()
    brands = content.split(',')
    map(lambda x: x.strip(), brands)
    phoneDBAdaper.updateAllBrandData(brands)
