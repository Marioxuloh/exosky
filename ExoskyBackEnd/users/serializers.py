from rest_framework import serializers
from .models import User

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']

class LoginUsuarioSerializer(serializers.Serializer):
    name = serializers.CharField()
