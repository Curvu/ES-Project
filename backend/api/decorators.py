from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import User, Token
from .utils import decode_token


def authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({"error": "Token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = Token.objects.filter(token=token).first()
            if not token.is_valid:
                return JsonResponse({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            decoded_token = decode_token(token.token)
            if not decoded_token:
                token.is_valid = False
                token.save()
                return JsonResponse({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(username=decoded_token['username']).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)

            return view_func(request, user=user, token=token.token, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return _wrapped_view


def validate_request(serializer_class):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            serializer = serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # Pass validated data as an extra kwarg, e.g. validated_data
            kwargs['payload'] = serializer.validated_data
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator
