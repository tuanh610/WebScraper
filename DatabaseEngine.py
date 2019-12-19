import boto3


dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')


def createTable():
    table = dynamodb.create_table(
        TableName='PriceList',
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


def pushDataToDB(data):
    table = dynamodb.Table('PriceList')

    table.put_item(
        Item={

        }
    )