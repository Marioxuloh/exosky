from rest_framework.response import Response
from rest_framework.views import APIView
from .services import get_exoplanets_data

class ExoplanetsDataView(APIView):
    def get(self, request):
        data = get_exoplanets_data()  # Lógica para consumir la API de Gaia
        return Response(data)
