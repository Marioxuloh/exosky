from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import RegistroUsuarioSerializer, LoginUsuarioSerializer
from django.db import IntegrityError

# Registro de usuario
class RegistroUserView(APIView):
    def post(self, request):
        user_name = request.data['name']
        try:
            user = User(
            name=user_name,
            )
            user.save()
            return Response({"mensaje": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
                return Response("user already exists",status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Login de usuario
class LoginUserView(APIView):
    def post(self, request):
        user_name = request.data['name']
        try:
            usuario = User.objects.get(name=user_name)
            return Response({"mensaje": "Login exitoso"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Usuario o contraseña incorrectos"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
