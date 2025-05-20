import datetime

def lambda_handler(event, context):
    current_time = datetime.datetime.fromisoformat(event['current_time'].replace('Z', '+00:00')) - datetime.timedelta(seconds=60)
    compared_time = datetime.datetime.fromisoformat(event['compared_time'].replace('Z', '+00:00'))

    return {
        'greater': current_time > compared_time
    }