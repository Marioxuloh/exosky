from django.urls import path
from .views import GaiaStarDetailsView, GaiaNearbyStarsView

urlpatterns = [
    path('stardetails/', GaiaStarDetailsView.as_view(), name='gaia-data'),
    path('nearbystars/', GaiaNearbyStarsView.as_view(), name='gaia-nearby-stars'),
]
