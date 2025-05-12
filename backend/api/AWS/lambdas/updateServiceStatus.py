import json

def lambda_handler(event, context):
    # Assume event contains the service ID and current state
    service_id = event.get('service_id')

    # Simulate the service status update (in real case, this could be a database operation)
    new_state = 4  # Mark the service as completed

    # Here we would update the service status in a real database
    print(f"Service {service_id} status updated to {new_state}")

    # Return the updated status or any other necessary data
    return {
        "status": "success",
        "service_id": service_id,
        "new_state": new_state
    }
