from django.urls import include, path
from apps.accounts.views import user_views, auth_views

app_name = "accounts"

urlpatterns = [
    path(
        "user/",
        include(
            [
                path(
                    "",
                    auth_views.UserGetAPIView.as_view(),
                    name="user-retrieve",
                ),
                path(
                    "register/",
                    auth_views.UserRegistrationAPIView.as_view(),
                    name="auth-register",
                ),
                path(
                    "login/", auth_views.UserLoginAPIView.as_view(), name="auth-login"
                ),
            ]
        ),
    ),
]
