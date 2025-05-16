from rest_framework.decorators import api_view
from django.http import JsonResponse
import base64
from ..utils import get_rekognition_client, require_params, authenticated, encode_token
from ..models import User, Token

@api_view(["POST"])
@require_params('images', 'name')
def force_register(request):
    try:
        name = request.data.get('name')
        images = request.data.get('images')

        if User.objects.filter(username=name).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)

        if not isinstance(images, list):
            return JsonResponse({'error': 'Images must be provided as a list'}, status=400)

        user = User.objects.create(username=name, is_admin=False)
        user.save()
        user_data = {'username': name, 'is_admin': False}
        token = encode_token(user_data)
        Token.objects.create(user=user, token=token)
        return JsonResponse({'token': token, 'user': user_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(["POST"])
def force_login(request):
    try:
        user = User.objects.filter(username='Filipe').first()
        user_data = {'username': user.username, 'is_admin': user.is_admin}
        token = encode_token(user_data)
        Token.objects.create(user=user, token=token)
        return JsonResponse({'token': token, 'user': user_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(["POST"])
@require_params('images', 'name')
def register(request):
    try:
        name = request.data.get('name')
        images = request.data.get('images')

        if User.objects.filter(username=name).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)

        if not isinstance(images, list):
            return JsonResponse({'error': 'Images must be provided as a list'}, status=400)

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
            Token.objects.create(user=user, token=token)
            return JsonResponse({'token': token, 'user': user_data}, status=200)

        return JsonResponse({'error': 'No face indexed'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(["POST"])
@require_params('image')
def login(request):
    try:
        #* Decode the base64 image
        image = request.data.get('image')
        image_data = base64.b64decode(image.split(',')[1])

        rekognition = get_rekognition_client()

        #* Invoke the Rekognition API
        response = rekognition.search_faces_by_image(
            CollectionId='my_collection',
            Image={'Bytes': image_data},
            FaceMatchThreshold=95,
            MaxFaces=1
        )

        #* Check if a face match was found
        if 'FaceMatches' in response and len(response['FaceMatches']) > 0:
            face_match = response['FaceMatches'][0]
            user = User.objects.filter(username=face_match['Face']['ExternalImageId']).first()
            user_data = {'username': user.username, 'is_admin': user.is_admin}
            token = encode_token(user_data)
            Token.objects.create(user=user, token=token)
            return JsonResponse({'token': token, 'user': user_data}, status=200)
        return JsonResponse({'error': 'No face match found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(["POST"])
@authenticated
def logout(request, user, token):
    token_obj = Token.objects.filter(token=token, is_valid=True, user=user).first()

    if token_obj:
        token_obj.is_valid = False
        token_obj.save()
        return JsonResponse({'message': 'Logged out successfully'}, status=200)
    return JsonResponse({'error': 'Token already inactive or invalid'}, status=400)


@api_view(["POST"])
def create_collection(request):
    try:
        rekognition = get_rekognition_client()
        response = rekognition.create_collection(CollectionId='my_collection')
        return JsonResponse({'message': 'Collection created successfully', 'response': response}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)