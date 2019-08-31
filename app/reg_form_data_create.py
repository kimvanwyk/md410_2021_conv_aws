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

def lambda_handler(data, context):
    try:
        client = boto3.client('s3')

        reg_num = int(list(update_reg_num()['Attributes']['RefNum'].values())[0])
        data['registration_number'] = reg_num
        fn = f'reg_forms/{reg_num:03}/data.json'
        client.put_object(Body=bytes(json.dumps(data), encoding='utf-8'), 
                          Bucket='md410-2020-conv', 
                          Key=fn)
        return f'md410-2020-conv/{fn}'
    except Exception as e:
        raise
