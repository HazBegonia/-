from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.get_recommendations, name = 'get_recommendations'),
]