# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('captcha/', views.get_captcha, name='captcha'),
    path('login/', views.login_api, name='login'),
    path('register/', views.register_api, name='register'),
    path('change_password/', views.change_password_api, name='change_password'),
]