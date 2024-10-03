from rest_framework.response import Response
from rest_framework.views import APIView
from .services import get_exoplanets_data

class ExoplanetsDataView(APIView):
    def get(self, request):
        try:
            data = get_exoplanets_data()
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)