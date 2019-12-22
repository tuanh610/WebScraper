class PhoneDataInvalidException(Exception):
    pass


class PhoneData:
    def __init__(self, name: str, price, info=None):
        if info is None:
            self.info = {}
        else:
            self.info = info
        self.name = name
        if isinstance(price, str):
            self.price = 0
            self.processPriceString(price)
        else:
            try:
                self.price = float(price)
            except Exception as e:
                raise PhoneDataInvalidException



    def processPriceString(self, priceStr: str):
        #find currency symbol
        temp = self.batchRemove(priceStr, ["$", ".", ","])
        splited = temp.split(sep=' ')
        splited_len = len(splited)
        try:
            if splited_len == 2:
                if (not splited[0].isdecimal()) and (not splited[1].isdecimal()):
                    raise PhoneDataInvalidException
                elif splited[0].isdecimal():
                    self.price = int(splited[0])
                    self.info["currency"] = splited[1]
                else:
                    self.price = int(splited[1])
                    self.info["currency"] = splited[0]
            elif splited_len == 1 and splited[0].isdecimal():
                self.price = int(splited[0])
                self.info["currency"] = "NA"
        except Exception as e:
            print(str(e))
            raise PhoneDataInvalidException

    def batchRemove(self, a: str, lst: [str]):
        temp = a
        for item in lst:
            temp = temp.replace(item, "")
        return temp

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getInfo(self):
        return self.info