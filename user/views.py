from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def login(request):
    if request.data.get('username') is None or request.data.get('password') is None:
        return Response({'status':False, 'message': 'Username and password are required'})
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token = Token.objects.get(user=user)
        return Response({'status':True, 'token':token.key})
    return Response({'status':False, 'message': 'Invalid credentials'})

@api_view(['POST'])
def register_user(request):
    if request.data.get('email') is None or request.data.get('password') is None:
        return Response({'status':False, 'message': 'Email and password are required'})
    email = request.data.get('email')
    password = request.data.get('password')
    role = "user"
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(username=email, email=email, password=password, role=role)
        user.save()
        token = Token.objects.create(user=user)
        return Response({'status':True, 'token':token.key})
    return Response({'status':False, 'message': 'Email already exists'})

@api_view(['POST'])
def register_admin(request):
    if request.data.get('email') is None or request.data.get('password') is None:
        return Response({'status':False, 'message': 'Email and password are required'})
    email = request.data.get('email')
    password = request.data.get('password')
    role = "admin"
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(username=email, email=email, password=password, role=role)
        user.save()
        token = Token.objects.create(user=user)
        return Response({'status':True, 'token':token.key})
    return Response({'status':False, 'message': 'Email already exists'})