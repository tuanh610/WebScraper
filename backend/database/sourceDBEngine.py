import boto3
from backend.scraping.SourceData import SourceData
from boto3.dynamodb.conditions import Attr
import backend.constant as constant
from botocore.exceptions import ClientError
import backend.database.DatabaseEngine as DatabaseEngine


class sourceDBEngine:
    def __init__(self):
        # Create Table if not exist, error handling already in create function
        DatabaseEngine.createTable(tableName=constant.sourceTableName, elements=constant.sourceElements)
        self.dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
        self.tableName = constant.sourceTableName
        self.table = self.dynamodb.Table(self.tableName)

    def pushAllDataToDB(self, data: [SourceData]):
        for source in data:
            self.table.put_item(
                Item={
                    'URL': source.url,
                    'TYPE': source.srcType,
                    'NAME': source.name,
                    'INFO': source.info
                }
            )
        print("Data pushed completed")

    def getAllDataFromTable(self):
        try:

            response = self.table.scan(
            )
            result = []
            for item in response['Items']:
                result.append(SourceData(url=item['URL'], name=item['NAME'], srctype=item['TYPE'], info=item['INFO']))
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])

    def getItemFromDB(self, sourceName: str):
        try:
            response = self.table.get_item(
                Key={
                    'NAME': sourceName
                }
            )
            item = response['Item']
            print("Get item successfully")
            return SourceData(url=item['URL'], name=item['NAME'], srctype=item['TYPE'], info=item['INFO'])
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ClientError
        except KeyError as e:
            print("Data is empty. No Item found")
            return None

    def updateItemToDB(self, item: SourceData):
        try:
            response = self.table.update_item(
                Key={
                    'NAME': item.name
                },
                UpdateExpression="set info = :i, url = :u, type = :t",
                ExpressionAttributeValues={
                    ':u': item.url,
                    ':i': item.info,
                    ':t': item.srcType
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("UpdateItem succeeded:")

    def deleteItemFromDB(self, item: SourceData):
        try:
            response = self.table.delete_item(
                Key={
                    'NAME': item.name
                },
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("DeleteItem succeeded:")
            #print(json.dumps(response, indent=4, cls=DecimalEncoder))
