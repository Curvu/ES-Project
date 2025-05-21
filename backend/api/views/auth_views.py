from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.decorators import authenticated, validate_request
from django.utils.decorators import method_decorator
import base64
from api.utils import get_rekognition_client, encode_token, get_auth_header_parameter
from api.models import User, Token
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.serializers import (
    RegisterRequestSerializer,
    LoginRequestSerializer,
    SignResponseSerializer,
)


class RegisterView(APIView):
    @extend_schema(
        summary="Register a new user",
        description="Registers a new user by indexing their face images in the Rekognition collection.",
        request=RegisterRequestSerializer,
        responses={
            200: SignResponseSerializer,
            400: OpenApiResponse(description="Bad request, e.g. user already exists or images not a list"),
            500: OpenApiResponse(description="Internal server error during Rekognition or DB ops")
        }
    )
    @validate_request(RegisterRequestSerializer)
    def post(self, request, payload):
        try:
            name = payload.get('name')
            images = payload.get('images')

            if User.objects.filter(username=name).exists():
                return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(images, list):
                return Response({'error': 'Images must be provided as a list'}, status=status.HTTP_400_BAD_REQUEST)

            rekognition = get_rekognition_client()
            successful_indices = 0

            for image in images:
                image_data = base64.b64decode(image.split(',')[1])

                response = rekognition.index_faces(
                    CollectionId='my_collection',
                    Image={'Bytes': image_data},
                    ExternalImageId=name,  # Same ID for all images of this person
                    DetectionAttributes=['ALL']
                )

                if 'FaceRecords' in response and len(response['FaceRecords']) > 0:
                    successful_indices += 1

            if successful_indices > 0:
                user = User.objects.create(username=name, is_admin=False)
                user.save()
                user_data = {'username': name, 'is_admin': False}
                token = encode_token(user_data)
                Token.objects.create(token=token)
                return Response({'token': token, 'user': user_data}, status=status.HTTP_200_OK)

            return Response({'error': 'No face indexed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    @extend_schema(
        summary="Login using face recognition",
        description="Logs in a user by searching for their face in the Rekognition collection.",
        request=LoginRequestSerializer,
        responses={
            200: SignResponseSerializer,
            404: OpenApiResponse(description="No face match found"),
            500: OpenApiResponse(description="Internal server error during Rekognition or DB ops")
        }
    )
    @validate_request(LoginRequestSerializer)
    def post(self, request, payload):
        try:
            image_data = base64.b64decode(payload.get('image').split(',')[1])

            rekognition = get_rekognition_client()

            response = rekognition.search_faces_by_image(
                CollectionId='my_collection',
                Image={'Bytes': image_data},
                MaxFaces=1,
                FaceMatchThreshold=95
            )

            if 'FaceMatches' in response and len(response['FaceMatches']) > 0:
                face_match = response['FaceMatches'][0]
                user = User.objects.filter(username=face_match['Face']['ExternalImageId']).first()
                user_data = {'username': user.username, 'is_admin': user.is_admin}
                token = encode_token(user_data)
                Token.objects.create(token=token)
                return Response({'token': token, 'user': user_data}, status=status.HTTP_200_OK)
            return Response({'error': 'No face match found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(authenticated, name='dispatch')
class LogoutView(APIView):
    @extend_schema(
        summary="Logout a user",
        description="Logs out a user by invalidating their JWT token.",
        parameters=get_auth_header_parameter(),
        responses={
            200: OpenApiResponse(description="Logged out successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            500: OpenApiResponse(description="Internal server error during DB ops")
        }
    )
    def post(self, request, user, token):
        try:
            Token.objects.filter(token=token).update(is_valid=False)
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)