import boto3
from backend.scraping.PhoneData import PhoneData, PhoneDataInvalidException
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

class phoneDBEngine:
    def __init__(self, tableName: str):
        self.dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
        self.tableName = tableName
        self.table = self.dynamodb.Table(self.tableName)

    def pushAllDataToDB(self, data: [PhoneData]):
        for phone in data:
            self.table.put_item(
                Item={
                    'NAME': phone.getName(),
                    'BRAND': phone.getBrand(),
                    'PRICE': phone.getPrice(),
                    'INFO': phone.getInfo()
                }
            )
        print("Data pushed completed")

    def getAllDataFromTable(self):
        try:

            response = self.table.scan(
                FilterExpression=Attr('PRICE').gt(0)
            )
            result = []
            for item in response['Items']:
                try:
                    result.append(PhoneData(item['NAME'], item['PRICE'], item['INFO'], item['BRAND']))
                except PhoneDataInvalidException as e:
                    print("Phone data invalid: " + item['NAME'] + ": " + item['PRICE'])
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])

    def getItemFromDB(self, phoneName: str):
        try:
            response = self.table.get_item(
                Key={
                    'NAME': phoneName
                }
            )
            item = response['Item']
            print("Get item successfully")
            return item
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ClientError
        except KeyError as e:
            print("Data is empty. No Item found")
            return None

    def updateItemToDB(self, item: PhoneData):
        try:
            response = self.table.update_item(
                Key={
                    'NAME': item.getName()
                },
                UpdateExpression="set INFO = :i, PRICE = :p, BRAND = :b",
                ExpressionAttributeValues={
                    ':p': item.getPrice(),
                    ':i': item.getInfo(),
                    ':b': item.getBrand()
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("UpdateItem succeeded:")
            #print(json.dumps(response, indent=4, cls=DecimalEncoder))

    def deleteItemFromDB(self, item: PhoneData):
        try:
            response = self.table.delete_item(
                Key={
                    'NAME': item.getName()
                },
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("DeleteItem succeeded:")
