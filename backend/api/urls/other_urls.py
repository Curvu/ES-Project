from django.urls import path
from api.views.other_views import (
    frontend,
)

urlpatterns = [
    path('', frontend, name='frontend')
]
