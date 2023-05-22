from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers


urlpatterns = [
    path("newuser/", views.AuthSerializerView.as_view(), name="newuser"),
    path("allusers/", views.AllCustomersView, name="allusers"),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]