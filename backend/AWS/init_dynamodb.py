import boto3

def create_service_status_table():
    # Use the client for administrative actions
    dynamodb_client = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        endpoint_url='http://localhost:4566/',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )

    existing_tables = dynamodb_client.list_tables()["TableNames"]
    if "ServiceStatus" not in existing_tables:
        dynamodb_client.create_table(
            TableName="ServiceStatus",
            KeySchema=[{"AttributeName": "service_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "service_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        # Wait for table to be active
        waiter = dynamodb_client.get_waiter("table_exists")
        waiter.wait(TableName="ServiceStatus")
        print("✅ Created DynamoDB table: ServiceStatus")

create_service_status_table()
