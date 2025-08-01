from dotenv import load_dotenv
import os
import boto3
load_dotenv()

IS_LOCAL = os.getenv('IS_LOCAL', 'false') == 'true'

def get_dynamodb_resource():
    if IS_LOCAL:
        return boto3.resource(
            'dynamodb',
            region_name='us-east-1',
            endpoint_url='http://localstack:4566',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )
    else:
        return boto3.resource('dynamodb', region_name='us-east-1')

dynamodb = get_dynamodb_resource()

service_status_table = dynamodb.Table('ServiceStatus')

def update_status(service_id, key, value):
    service_status_table.update_item(
        Key={'service_id': str(service_id)},
        UpdateExpression=f'SET {key} = :val',
        ExpressionAttributeValues={':val': value}
    )

def get_status(service_id):
    response = service_status_table.get_item(Key={'service_id': str(service_id)})
    return response.get('Item')
