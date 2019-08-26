import json

import boto3

client = boto3.client('dynamodb')
def update_reg_num():
    response = client.update_item(
    TableName='MDConv2020RefNum',
    Key={
        'ID': {
            'N': '1'
            }
        },
    ReturnValues='ALL_NEW',
    UpdateExpression='SET RefNum = RefNum + :r',
    ExpressionAttributeValues={
        ':r': {
            'N': '1',
            }
        }
    )
    return response

def lambda_handler(event, context):
    try:
        d = event['data']
        resp = update_reg_num()
        d['registration_number'] = list(resp['Attributes']['RefNum'].values())[0]
        retcode = 200
    except Exception as e:
        retcode = 400
    return {"statusCode": retcode}

