from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import LogoutView

app_name = "users_app"

urlpatterns = [
    path("account/login/", TokenObtainPairView.as_view(), name="token_login"),
    path("account/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("account/logout/", LogoutView.as_view(), name="auth_logout"),
]
