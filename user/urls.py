from django.urls import path
from .views import *

urlpatterns = [
    path('register_admin',register_admin), # Register Admin
    path('register_user',register_user), # Register User
    path('login', login), # Login
]