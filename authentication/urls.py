from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView


urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    # path('user/register/', UserRegisterView.as_view(), name='user-register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('users/', UersView.as_view(), name='users'),
]