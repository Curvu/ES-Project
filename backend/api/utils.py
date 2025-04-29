from functools import wraps
from django.http import JsonResponse
import boto3
from jwt import encode, decode
from .models import Users, Token
import os
from dotenv import load_dotenv
load_dotenv()


def get_rekognition_client():
    return boto3.client(
        'rekognition',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('aws_access_key_id'),
        aws_secret_access_key=os.getenv('aws_secret_access_key'),
        aws_session_token=os.getenv('aws_session_token')
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


def authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({"error": "Token not provided"}, status=401)

        try:
            decoded_token = decode_token(token)
            # search for the user in the database for face_id
            if not decoded_token:
                return JsonResponse({"error": "Invalid token"}, status=401)

            user = Users.objects.filter(username=decoded_token['username']).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=401)

            if not Token.objects.filter(user=user, token=token, is_valid=True).exists():
                return JsonResponse({"error": "Token is inactive or logged out"}, status=401)

            return view_func(request, user=user, token=token, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=401)
    return _wrapped_view


def encode_token(data):
    """
    Generate a JWT token for the given user.
    """
    token = encode(data, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
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