from rest_framework import serializers
from django.db import models
from django.contrib.auth.hashers import make_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):

        user = User.objects.create_user(
            validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
