from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import Register, TokenObtainPairViewCustom

urlpatterns = [
    path('token', TokenObtainPairViewCustom.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', Register.as_view(), name='login'),
]
