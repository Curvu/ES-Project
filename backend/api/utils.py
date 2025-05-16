import boto3
from jwt import encode, decode
import os
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from dotenv import load_dotenv
load_dotenv()

IS_LOCAL = os.getenv('IS_LOCAL', 'false') == 'true'

def get_rekognition_client() -> boto3.client:
    return boto3.client(
        'rekognition',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('aws_access_key_id'),
        aws_secret_access_key=os.getenv('aws_secret_access_key'),
        aws_session_token=os.getenv('aws_session_token')
    )

def get_stepfunctions_client() -> boto3.client:
    if IS_LOCAL:
        return boto3.client(
            'stepfunctions',
            region_name='us-east-1',
            endpoint_url='http://localstack:4566',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )
    else:
        return boto3.client(
            'stepfunctions',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('aws_access_key_id'),
            aws_secret_access_key=os.getenv('aws_secret_access_key'),
            aws_session_token=os.getenv('aws_session_token')
        )


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


def get_auth_header_parameter():
    return [
        OpenApiParameter(
            name='Authorization',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            required=True,
            description='JWT token. Format: <your_token>'
        )
    ]
