import copy
from django.shortcuts import render
from django.http import HttpResponse , JsonResponse

from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from Auth.models import UserDetails
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db import transaction


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        dob = data.get('dob')
        address = data.get('address')
        account_location = data.get('account_location')
        userid = data.get('userid')
        password = data.get('password')
        email = data.get('email')  # get email from request data

        if not name or not dob or not address  or not userid or not password or not email:  # check if email is provided
            return Response({'error': 'Please provide all fields'}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=userid, password=password, email=email)  # set email for User

        print(user , "user")
        user = UserDetails.objects.create(
            user=user,
            name=name,
            dob=dob,
            address=address,
            account_location=account_location,
            email=email,  # set email for UserDetails
        )

        return Response({'message': 'User created successfully'}, status=HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        userid = data.get('userid')
        password = data.get('password')

        
        if not userid or not password:
            print(data)
            return Response({'error': 'Please provide both userid and password'}, status=HTTP_400_BAD_REQUEST)

        user = authenticate(username=userid, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=HTTP_400_BAD_REQUEST)
        
        token , created = Token.objects.get_or_create(user=user)
        
        user_info = UserDetails.objects.get(user=user)
        # Return the access token and user data
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': {
                'userid': user.username,
                'name': user_info.name,
                'dob': user_info.dob,
                'email': user_info.email,  # add email to the response
            }
        }, status=HTTP_200_OK)
    

    
class UpdateInformation(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        data = request.data
        name = data.get('name')
        dob = data.get('dob')
        address = data.get('address')
        account_location = data.get('account_location')
        
        phone = data.get('phone')
        userid = request.user.username
        email = data.get('email')
        print(data)
        if not name or not dob or not address or not account_location or not phone or not email:
            return Response({'error': 'Please provide any one to update fields'}, status=HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=userid)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=HTTP_400_BAD_REQUEST)
        
        user_info = UserDetails.objects.get(user=user)
        
        user_info.name = name
        user_info.dob = dob
        user_info.address = address
        user_info.account_location = account_location
        user_info.phone = phone
        user_info.email = email
        user_info.save()
        
        return Response({'message': 'User information updated successfully'}, status=HTTP_200_OK)

class GetUserDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        user_info = UserDetails.objects.get(user=user)
        
        return Response({
            'userid': user.username,
            'name': user_info.name,
            'dob': user_info.dob,
            'address': user_info.address,
            'account_location': user_info.account_location,
            'phone': user_info.phone,
            'email': user_info.email,   
        }, status=HTTP_200_OK)