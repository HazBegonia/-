from django.urls import path
from .views import suggest_api

urlpatterns = [
    path('api/suggest/', suggest_api),
]