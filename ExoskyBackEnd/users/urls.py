from django.urls import path
from users.views import *

urlpatterns = [
    path('', UsersDataView.as_view(), name='create-user'),
]