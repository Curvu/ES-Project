from functools import wraps
from django.http import JsonResponse
import boto3
from jwt import encode, decode
# import datetime
import os
from dotenv import load_dotenv
load_dotenv()


def get_rekognition_client():
    return boto3.client(
        'rekognition',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )


def require_params(*required_params):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            missing = [p for p in required_params if not request.data.get(p)]
            if missing:
                return JsonResponse(
                    {'error': f"Missing parameters: {', '.join(missing)}"},
                    status=400
                )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def encode_token(data):
    """
    Generate a JWT token for the given user.
    """

    token = encode(data, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    # exp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    return token

def decode_token(token):
    """
    Decode the JWT token and return the payload.
    """
    try:
        payload = decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        return payload
    except:
        return None