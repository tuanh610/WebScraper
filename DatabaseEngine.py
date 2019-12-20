import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import json
from PhoneData import PhoneData



class dynammoDBAdapter:

    def __init__(self, tableName: str):
        self.dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
        self.tableName = tableName

    def createTable(self):
        table = self.dynamodb.create_table(
            TableName=self.table_name,
            keySchema=[
                {
                    'AttributeName': 'DeviceName',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'price',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'DeviceName',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'price',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 3,
                'WriteCapacityUnits': 3
            }
        )

        table.meta.client_get_waiter('table_exist').wait(TableName='PriceList')
        print(table.item_count)

    def pullDataFromDB(self, tableName: str):
        table = self.dynamodb.Table(tableName)
        response = table.get_item(

        )


    def pushAllDataToDB(self, tableName: str, data: [PhoneData]):
        table = self.dynamodb.Table(tableName)
        for phone in data:
            table.put_item(
                Item={
                    'DeviceName': phone.getName(),
                    'price': phone.getPrice(),
                    'info': phone.getInfo()
                }
            )
        print("Data pushed completed")


    def getItemFromDB(self, tableName: str,phoneName: str):
        table = self.dynamodb.Table(tableName)
        try:
            response = table.get_item(
                Key={
                    'DeviceName': phoneName
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Item']
            print("Get item successfully")

    def updateItemToDB(self, item: PhoneData):
        

