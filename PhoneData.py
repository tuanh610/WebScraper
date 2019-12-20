class PhoneDataInvalidException(Exception):
    pass


class PhoneData:
    def __init__(self, name: str, price: int, info):
        self.name = name
        self.price = price
        self.info = info

    def processPriceString(self, priceStr: str):
        #find currency symbol
        temp = priceStr.replace("$", " ")
        splited = temp.split(sep=' ')
        splited_len = len(splited)
        if splited_len == 2:
            if (not splited[0].isdecimal()) and (not splited[1].isdecimal()):
                raise PhoneDataInvalidException
            elif splited[0].isdecimal():
                self.price = data
