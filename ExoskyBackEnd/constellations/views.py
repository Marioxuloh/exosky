from rest_framework.response import Response
from rest_framework.views import APIView
from .services import get_constellations, insert_constellation

class ConstellationsDataView(APIView):
    def post(self, request):
        try:
            constellations = get_constellations(request.data.get('pl_name'))
            return Response(constellations)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class ConstellationsInsertDataView(APIView):
    def post(self, request):
        try:
            user_name = request.data.get('user_name')
            exoplanet_name = request.data.get('pl_name')
            constellation = request.data.get('coordenates')
            constellations = insert_constellation(user_name, exoplanet_name, constellation)
            return Response(constellations)
        except Exception as e:
            return Response({"error": str(e)}, status=500)