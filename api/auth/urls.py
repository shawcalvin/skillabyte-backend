from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from .views import RegisterView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="token_obtain_pair"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
]