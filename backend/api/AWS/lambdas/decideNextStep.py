import boto3
from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    service_status_table = dynamodb.Table('ServiceStatus')

    service_id = event.get('service_id')
    schedule_time = event.get('schedule_time')

    # Get current status
    response = service_status_table.get_item(
        Key={'service_id': service_id}
    )

    state = response['Item']['service_state']
    paid = response['Item']['paid']

    if state == 4 and paid:
        # update the state to 5 (completed)
        service_status_table.update_item(
            Key={'service_id': service_id},
            UpdateExpression='SET service_state = :val',
            ExpressionAttributeValues={
                ':val': 5
            }
        )
        return { "recheck": False, "message": "Success" }

    # Check if the service is already passed
    if schedule_time < datetime.now().isoformat() and state == 1:
        service_status_table.update_item(
            Key={'service_id': service_id},
            UpdateExpression='SET service_state = :val',
            ExpressionAttributeValues={
                ':val': -1
            }
        )
        return { "recheck": False, "message": "Already passed" }

    return { "recheck": True, "service_id": service_id, "schedule_time": schedule_time }