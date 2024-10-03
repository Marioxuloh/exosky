from rest_framework import serializers
from .models import User

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'password']

class LoginUsuarioSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    password = serializers.CharField()
