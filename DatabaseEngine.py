import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import json
from PhoneData import PhoneData
from PhoneData import PhoneDataInvalidException
import decimal


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def createTable(tableName: str):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    try:
        table = dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': 'DeviceName',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'DeviceName',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 3,
                'WriteCapacityUnits': 3
            }
        )
        table.meta.client_get_waiter('table_exist').wait(TableName='PriceList')
        print(table.item_count)
    except ClientError as e:
        if e.response['Error']['Code'] == "ResourceNotFoundException":
            print("Table " + tableName + " already existed")
        else:
            print(e.response['Error']['Message'])


class dynammoDBAdapter:

    def __init__(self, tableName: str):
        self.dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
        self.tableName = tableName
        self.table = self.dynamodb.Table(self.tableName)

    def pullDataFromDB(self):
        response = self.table.get_item(

        )


    def pushAllDataToDB(self, data: [PhoneData]):
        for phone in data:
            self.table.put_item(
                Item={
                    'DeviceName': phone.getName(),
                    'price': phone.getPrice(),
                    'info': phone.getInfo()
                }
            )
        print("Data pushed completed")

    def getAllDataFromTable(self):
        try:

            response = self.table.scan(
                FilterExpression=Attr('price').gt(0)
            )
            result = []
            for item in response['Items']:
                try:
                    result.append(PhoneData(item['DeviceName'], item['price'], item['info']))
                except PhoneDataInvalidException as e:
                    print("Phone data invalid: " + item['DeviceName'] + ": " + item['price'])
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])

    def getItemFromDB(self, phoneName: str):
        try:
            response = self.table.get_item(
                Key={
                    'DeviceName': phoneName
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Item']
            print("Get item successfully")
            print(json.dumps(item, indent=4, cls=DecimalEncoder))

    def updateItemToDB(self, item: PhoneData):
        try:
            response = self.table.update_item(
                Key={
                    'DeviceName': item.getName()
                },
                UpdateExpression="set info = :i, price = :p",
                ExpressionAttributeValues={
                    ':p': item.getPrice(),
                    ':i': item.getInfo()
                },
                ReturnValues="UPDATED_NEW"
            )
        except Exception as e:
            print(e.response['Error']['Message'])
        else:
            print("UpdateItem succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))

    def deleteItemFromDB(self, item:PhoneData):
        try:
            response = self.table.delete_item(
                Key={
                    'DeviceName': item.getName()
                },
            )
        except Exception as e:
            print(e.response['Error']['Message'])
        else:
            print("DeleteItem succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))

