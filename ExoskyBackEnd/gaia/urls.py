from django.urls import path
from .views import GaiaDataView

urlpatterns = [
    path('data/', GaiaDataView.as_view(), name='gaia-data'),
]
