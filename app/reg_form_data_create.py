import json

import boto3

client = boto3.client('dynamodb')
def update_reg_num(num=1):
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

def lambda_handler(data, context):
    try:
        client = boto3.client('s3')

        num = 1 if data['partner'] == 'partner_none' else 2

        reg_num = update_reg_num(num)
        data['registration_number'] = reg_num
        fn = f'reg_forms/{reg_num:03}/data.json'
        client.put_object(Body=bytes(json.dumps(data), encoding='utf-8'), 
                          Bucket='md410-2020-conv', 
                          Key=fn)
        return f'md410-2020-conv/{fn}'
    except Exception as e:
        raise
