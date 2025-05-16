from datetime import datetime, timedelta

def lambda_handler(event, context):
    service_id = event.get('service_id')
    schedule_time = event.get('schedule_time')
    sstate = int(event.get('sstate'))
    paid = event.get('paid')

    # Add 30 seconds to the schedule time
    schedule_time_dt = datetime.fromisoformat(schedule_time.replace("Z", "+00:00")) + timedelta(seconds=30)
    schedule_time = schedule_time_dt.isoformat()

    if sstate == 4 and paid:
        return { "recheck": 0, "service_id": service_id }
    elif not paid and schedule_time < datetime.now().isoformat():
        return { "recheck": -1, "service_id": service_id }

    return {
        "recheck": 1,
        "service_id": service_id,
        "schedule_time": schedule_time
    }
