from django.urls import path
from .views import RegistroUserView, LoginUserView

urlpatterns = [
    path('register/', RegistroUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
]
