from django.urls import path
from .views import ConstellationsDataView, ConstellationsInsertDataView

urlpatterns = [
    path('constellationsbyexoplanet/', ConstellationsDataView.as_view(), name='constellations-data'),
    path('constellationinsert/', ConstellationsInsertDataView.as_view(), name='constellations-data'),
]