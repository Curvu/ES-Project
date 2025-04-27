from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .rekognition_utils import get_rekognition_client
import base64

@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello World"})

@api_view(["POST"])
def register(request):
    try:
        #* Extract the base64 image from the request
        image_data = request.data.get('image')
        if not image_data:
            return JsonResponse({'error': 'No image provided'}, status=400)

        name = request.data.get('name')
        if not name:
            return JsonResponse({'error': 'No name provided'}, status=400)

        #* Decode the base64 image
        image_data = image_data.split(',')[1]  # Remove the metadata part
        image_data = base64.b64decode(image_data)

        #* Get the Rekognition client
        rekognition = get_rekognition_client()

        # rekognition.create_collection(CollectionId='my_collection') # Only run once to create the collection

        #* Invoke the Rekognition API
        response = rekognition.index_faces(
            CollectionId='my_collection',
            Image={'Bytes': image_data},
            ExternalImageId=name,
            DetectionAttributes=['ALL']
        )

        # TODO: check if name already exists in db

        #* Check if a face was indexed successfully
        if 'FaceRecords' in response and len(response['FaceRecords']) > 0:
            return JsonResponse({'message': 'Face indexed successfully'}, status=200)
        return JsonResponse({'error': 'No face indexed'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(["POST"])
def login(request):
    try:
        #* Extract the base64 image from the request
        image_data = request.data.get('image')
        if not image_data:
            return JsonResponse({'error': 'No image provided'}, status=400)

        # return JsonResponse({'message': 'Image received successfully'}, status=200)

        #* Decode the base64 image
        image_data = image_data.split(',')[1]  # Remove the metadata part
        image_data = base64.b64decode(image_data)
        # return JsonResponse({'message': 'Image data decoded successfully'}, status=200)

        #* Get the Rekognition client
        rekognition = get_rekognition_client()
        # return JsonResponse({'message': 'Rekognition client created successfully'}, status=200)

        #* Invoke the Rekognition API
        response = rekognition.search_faces_by_image(
            CollectionId='my_collection',
            Image={'Bytes': image_data},
            FaceMatchThreshold=95,
            MaxFaces=1
        )

        # TODO: jwt token!

        #* Check if a face match was found
        if 'FaceMatches' in response and len(response['FaceMatches']) > 0:
            face_match = response['FaceMatches'][0]
            face_id = face_match['Face']['FaceId']
            similarity = face_match['Similarity']
            external_image_id = face_match['Face']['ExternalImageId']
            return JsonResponse({'face_id': face_id, 'similarity': similarity, 'external_image_id': external_image_id}, status=200)
        return JsonResponse({'error': 'No face match found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)