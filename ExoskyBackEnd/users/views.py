from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import RegistroUsuarioSerializer, LoginUsuarioSerializer

# Registro de usuario
class RegistroUserView(APIView):
    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login de usuario
class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                usuario = User.objects.get(first_name=serializer.data['first_name'], password=serializer.data['password'])
                return Response({"mensaje": "Login exitoso"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Usuario o contraseña incorrectos"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
