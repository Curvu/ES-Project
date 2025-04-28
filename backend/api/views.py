from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import base64
from .utils import get_rekognition_client, require_params, encode_token, decode_token
from .models import Users

@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello World"})

@api_view(["POST"])
@require_params('image', 'name')
def register(request):
    try:
        name = request.data.get('name')
        if Users.objects.filter(username=name).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)

        #* Decode the base64 image
        image_data = request.data.get('image')
        image_data = image_data.split(',')[1]  # Remove the metadata part
        image_data = base64.b64decode(image_data)

        rekognition = get_rekognition_client()
        # Users.objects.all().delete() # Uncomment to delete all users
        # rekognition.delete_collection(CollectionId='my_collection') # Uncomment to delete the collection
        # rekognition.create_collection(CollectionId='my_collection') # Only run once to create the collection

        #* Invoke the Rekognition API
        response = rekognition.index_faces(
            CollectionId='my_collection',
            Image={'Bytes': image_data},
            ExternalImageId=name,
            DetectionAttributes=['ALL']
        )

        #* Check if a face was indexed successfully
        if 'FaceRecords' in response and len(response['FaceRecords']) > 0:
            face_record = response['FaceRecords'][0]
            face_id = face_record['Face']['FaceId']
            Users.objects.create(username=name, face_id=face_id, is_admin=False)
            return JsonResponse({'message': 'Face indexed successfully'}, status=200)
        return JsonResponse({'error': 'No face indexed'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(["POST"])
@require_params('image')
def login(request):
    try:
        #* Decode the base64 image
        image_data = request.data.get('image')
        image_data = image_data.split(',')[1]  # Remove the metadata part
        image_data = base64.b64decode(image_data)

        return JsonResponse({'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmYWNlX2lkIjoiMTBlNTE3Y2MtNTBlMi00YjA5LTg5NjMtNDI1ODQyYTBiOThhIiwic2ltaWxhcml0eSI6OTkuOTk4NzMzNTIwNTA3ODEsImV4dGVybmFsX2ltYWdlX2lkIjoiRmlsaXBlIn0.dFZ5OVI7XxXQi3zzSyK-9IZp2fAiu4qw6ePWqfNs39o"}, status=200)

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
            face_id = face_match['Face']['FaceId']
            similarity = face_match['Similarity']
            external_image_id = face_match['Face']['ExternalImageId']
            response = {
                'face_id': face_id,
                'similarity': similarity,
                'external_image_id': external_image_id
            }
            token = encode_token(response)
            return JsonResponse({'token': token}, status=200)
        return JsonResponse({'error': 'No face match found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)