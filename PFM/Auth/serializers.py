import traceback

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from Auth.models import UserDetails


class UserSerializer(serializers.ModelSerializer):

    userid = serializers.CharField(max_length=200)

    class Meta:
        model = UserDetails
        fields = '__all__'
        

