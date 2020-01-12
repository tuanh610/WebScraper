import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import json
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


class DynamoElement:
    def __init__(self, name, kType, attrType):
        self.name = name
        self.kType = kType
        self.attrType = attrType

    def get_schemaElement(self):
        return {
            'AttributeName': self.name,
            'KeyType': self.kType
        }

    def get_attributeElement(self):
        return {
            'AttributeName': self.name,
            'AttributeType': self.attrType
        }


def createTable(tableName: str, elements: [DynamoElement]):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    try:
        table = dynamodb.create_table(
            TableName=tableName,
            KeySchema=[x.get_schemaElement() for x in elements],
            AttributeDefinitions=[x.get_attributeElement() for x in elements],
            ProvisionedThroughput={
                'ReadCapacityUnits': 3,
                'WriteCapacityUnits': 3
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=tableName)
    except ClientError as e:
        if e.response['Error']['Code'] == "ResourceNotFoundException":
            print("Table " + tableName + " already existed")
        else:
            print(e.response['Error']['Message'])
    else:
        return "Create table " + tableName + "successfully"


def deleteTable(tableName: str):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(tableName)
    try:
        table.delete()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return "Delete table " + tableName + " successfully"
