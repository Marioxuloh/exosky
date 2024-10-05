from django.urls import path
from .views import ExoplanetsDataView

urlpatterns = [
    path('getall/', ExoplanetsDataView.as_view(), name='exoplanets-data'),
]
