from rest_framework.response import Response
from rest_framework.views import APIView
from .services import get_exoplanets_data, save_exoplanets_data, get_random_exoplanets_data

class ExoplanetsDataSaveView(APIView):
    def get(self, request):
        try:
            data = save_exoplanets_data()
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class ExoplanetsDataView(APIView):
    def get(self, request):
        try:
            data = get_exoplanets_data()
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
class ExoplanetsRandomDataView(APIView):
    def post(self, request):
        try:
            data = get_random_exoplanets_data(request.data.get('limit'))
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)