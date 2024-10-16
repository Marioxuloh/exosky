from django.urls import path
from .views import ExoplanetsDataSaveView, ExoplanetsDataView, ExoplanetsRandomDataView, ExoplanetsByIdDataView

urlpatterns = [
    path('getallandsave/', ExoplanetsDataSaveView.as_view(), name='exoplanets-data'),
    path('getallfrombd/', ExoplanetsDataView.as_view(), name='exoplanets-data'),
    path('getrandomfrombd/', ExoplanetsRandomDataView.as_view(), name='exoplanets-randomdata'),
    path('getbyname/', ExoplanetsByIdDataView.as_view(), name='exoplanets-byid'),
]
