import boto3
from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    service_status_table = dynamodb.Table('ServiceStatus')

    service_id = event.get('service_id')

    try:
        # Create DynamoDB entry
        service_status_table.put_item(
            Item={
                'service_id': service_id,
                'service_state': 1,
                'paid': False,
                'delivered': False
            }
        )

        # Return success
        return {
            "service_id": service_id,
            "failed": False
        }
    except Exception as e:
        return {
            "error": str(e),
            "failed": True
        }