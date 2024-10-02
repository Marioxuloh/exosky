from django.urls import path
from .views import ExoplanetsDataView

urlpatterns = [
    path('data/', ExoplanetsDataView.as_view(), name='exoplanets-data'),
]
