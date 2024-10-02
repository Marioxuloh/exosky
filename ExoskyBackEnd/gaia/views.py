from rest_framework.response import Response
from rest_framework.views import APIView
from .services import get_gaia_data

class GaiaDataView(APIView):
    def get(self, request):
        data = get_gaia_data()  # Lógica para consumir la API de Gaia
        return Response(data)
