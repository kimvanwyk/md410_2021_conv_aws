import boto3

if __name__ == '__main__':
    session = boto3.Session(profile_name='mdconv2020_s3')
    client = session.client('ses', region_name='eu-west-1')
else:
    client = boto3.client('ses')

def send_email(reg_num):
    response = client.send_email(
        Source='admin@lionsconvention2020.co.za',
        Destination={
            'ToAddresses': [
                'vanwykk+mdc2020@gmail.com',
            ],
        },
        Message={
            'Subject': {
                'Data': f'MDC 2020 Registration Form Received: {reg_num:04}',
            },
            'Body': {
                'Text': {
                    'Data': f'MDC 2020 Registration Form Received: {reg_num:04}',
                }
            }
        },
    )
    return response

if __name__ == '__main__':
    import sys
    send_email(int(sys.argv[1]))
