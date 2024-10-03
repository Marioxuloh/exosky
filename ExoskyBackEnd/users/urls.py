from django.urls import path
from .views import RegistroUserView, LoginUserView

urlpatterns = [
    path('registro/', RegistroUserView.as_view(), name='registro'),
    path('login/', LoginUserView.as_view(), name='login'),
]
