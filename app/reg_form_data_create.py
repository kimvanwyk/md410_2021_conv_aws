import datetime
import json

import send_email

import boto3

def update_reg_num(num=1):
    client = boto3.client('dynamodb')
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
            'N': "1",
            }
        }
    )
    reg_num = int(list(response['Attributes']['RefNum'].values())[0])
    if num > 1:
        client.update_item(
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
                'N': f"{num-1}",
                }
            }
        )
    return reg_num

def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3')
        data = json.loads(event['body'])['data']
        num = 1 if data['partner'] == 'partner_none' else 2

        reg_num = update_reg_num(num)
        data['registration_number'] = reg_num
        data['timestamp'] = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime('%y/%m/%d %H:%M:%S')
        fn = f'reg_forms/{reg_num:03}/data.json'
        s3_client.put_object(Body=bytes(json.dumps(data), encoding='utf-8'), 
                          Bucket='md410-2020-conv', 
                          Key=fn)
        send_email.send_email(reg_num)
        return {"statusCode": 200, "body": json.dumps({"reg_num": reg_num})}
    except Exception as e:
        raise
