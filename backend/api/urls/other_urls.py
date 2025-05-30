from django.urls import path, re_path
from api.views.other_views import (
    frontend,
)

urlpatterns = [
    path('', frontend, name='frontend'),
    re_path(r'^(?!api/).*$', frontend, name='frontend'),
]