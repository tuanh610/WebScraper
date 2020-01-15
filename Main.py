from backend.mail.mailingModule import mailModule
import backend.constant as constant
from backend.database.phoneDBEngine import phoneDBEngine

def masterUpdate():
    ChangesToNotify = {}
    phoneDBAdaper = phoneDBEngine(constant.dynamoDBTableName)

    # Loop through each source to update information
    for src in constant.scrapingSources:
        if src.name in constant.parser:
            parser = constant.parser[src.name](src.info.ignoreTerm, src.url, src.info.param)
            data = parser.getAllPages()

            # Update data for each source
            dataFromDB = phoneDBAdaper.getAllDataFromTable()
            updateNeeded = []
            newItem = []
            # Update data
            for item in data:
                existed = False
                for phone in dataFromDB:
                    if item.getName() == phone.getName():
                        if item != phone:
                            updateNeeded.append((item, phone))
                        existed = True
                        break
                if not existed:
                    newItem.append(item)

            # push new data to database
            for item, _ in updateNeeded:
                phoneDBAdaper.updateItemToDB(item)

            if len(newItem) > 0:
                phoneDBAdaper.pushAllDataToDB(newItem)

            # Add changes to notify list
            ChangesToNotify[src.name] = (newItem, updateNeeded)
        else:
            print("Parser for " + src.name + " is not available. Skip")
    return ChangesToNotify


def notifyByEmail(changes):
    content = ""
    for src in changes:
        content += "Update for %s:\n" % src
        newItem, updateNeeded = changes[src]
        if len(newItem) > 0:
            content += "New Items:\n"
            for item in newItem:
                info = item.getInfo()
                content += "Name: %s. Price: %d %s\n" % (item.getName(), item.getPrice(), info["currency"])
                if "url" in info:
                    content += "URL: %s\n" % info["url"]
        if len(updateNeeded) > 0:
            content += "Price Change Items:\n"
            for item, oldItem in updateNeeded:
                info = item.getInfo()
                oldInfo = oldItem.getInfo()
                content += "Name: %s. Old price: %d %s. New Price: %d %s\n" % (item.getName(),
                                                                               oldItem.getPrice(),
                                                                               oldInfo["currency"],
                                                                               item.getPrice(), info["currency"])
        if content == "":
            content = "No update needed"
        content += "================================================================\n"

    mail = mailModule()
    service = mail.getCredential()
    message = mail.create_message("warmboy610@gmail.com", "tuanh.dang610@gmail.com", "Update Price", content)
    result = mail.send_message(service, message)
    print(result)


"""
NotifyByEmail is false as I do not include the credentials and tokens of my Gmail account here 
Once the project is pulled from the projects, please use the link in mailingModule to get your
credentials.json file. Then enable this code by set notifyByEmail to true
"""
notify = False
changeToSend = masterUpdate()
if notify:
    notifyByEmail(changeToSend)
print("done")
