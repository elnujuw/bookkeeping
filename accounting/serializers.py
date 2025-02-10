from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BookkeepingRecord, ApiKey

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class BookkeepingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookkeepingRecord
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ['id', 'key', 'created_at']
        read_only_fields = ['id', 'key', 'created_at']