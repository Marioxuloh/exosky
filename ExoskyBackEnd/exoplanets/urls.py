from django.urls import path
from .views import ExoplanetsDataView

urlpatterns = [
    path('getrandom/', ExoplanetsDataView.as_view(), name='exoplanets-randomdata'),
    path('getall/', ExoplanetsDataView.as_view(), name='exoplanets-data'),
]
