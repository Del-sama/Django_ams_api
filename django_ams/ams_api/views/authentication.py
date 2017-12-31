# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_jwt.settings import api_settings

from ..serializers import UserSerializer, ProfileSerializer, LoginSerializer

def create_jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


class RegisterUsers(APIView):
    
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        profile_serializer = ProfileSerializer(data=request.data)
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            user.profile.role = profile_serializer.data['role']
            user.profile.faculty = profile_serializer.data['faculty']
            user.profile.department = profile_serializer.data['department']

            formatted_data = {
                "first name": user_serializer.data['first_name'],
                "last name": user_serializer.data['last_name'],
                "username": user_serializer.data['username'],
                "email" : user_serializer.data['email'],
                "role": profile_serializer.data['role'],
                "faculty": profile_serializer.data['faculty'],
                "department": profile_serializer.data['department']
            }

            token = create_jwt_token(user)
            if 'matric_number' in request.data:
                user.profile.matric_number = request.data['matric_number']
                formatted_data["matric_number"] = user.profile.matric_number
            else:
                pass
            return Response(
                {
                    "data": formatted_data,
                    "token": token
                }, status=status.HTTP_201_CREATED)
        elif not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUsers(APIView):

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            username = login_serializer.data['username']
            password = login_serializer.data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token = create_jwt_token(user)
                return Response(
                    { 
                        "message": "User successfully logged in",
                        "token": token 
                    }, 
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    { "message": "User not found" }, 
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUsers(APIView):
    
    def post(self, request):
        
        return Response(
            {"message": "User successfully logged out"},
             status=status.HTTP_200_OK)
