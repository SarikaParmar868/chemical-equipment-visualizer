from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EquipmentBatch

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class EquipmentBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentBatch
        fields = '__all__'
