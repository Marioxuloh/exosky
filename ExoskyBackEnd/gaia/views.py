from rest_framework.response import Response
from rest_framework.views import APIView
from .services import get_star_details, get_nearby_stars
import transversal.utils as utils

class GaiaStarDetailsView(APIView):
    def post(self, request):
        star_designations = request.data.get('star_designations', [])
        print(request.data)
        data = []
        for star_designation in star_designations:
            star_details = get_star_details(star_designation)
            data.append(star_details)
        return Response(data)

class GaiaNearbyStarsView(APIView):
    def post(self, request):
        ra = request.data.get('ra')
        dec = request.data.get('dec')
        parallax = request.data.get('parallax')
        visible_distance = request.data.get('visible_distance')
        n_stars = request.data.get('n_stars')
        ra = utils.sanitize_float(ra)
        dec = utils.sanitize_float(dec)
        parallax = utils.sanitize_float(parallax)
        visible_distance = utils.sanitize_float(visible_distance)
        nearby_stars = get_nearby_stars(ra, dec, parallax, visible_distance, n_stars)
        return Response(nearby_stars)