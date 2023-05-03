from django.urls import include, path
from apps.accounts.views import user_views

app_name = "accounts"

urlpatterns = [
    path(
        "user/",
        include(
            [
                path(
                    "",
                    user_views.UserRetrieveGenericAPIView.as_view(),
                    name="user-retrieve",
                )
            ]
        ),
    ),
]
