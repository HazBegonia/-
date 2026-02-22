# Books_web/my_profile/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.get_user_info, name='user_info'),
    path('history/', views.get_search_history, name='search_history'),
    path('collections/', views.get_my_collections, name='my_collections'),
    path('toggle/', views.toggle_collection, name='toggle_collection'),
]