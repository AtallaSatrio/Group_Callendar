from django.urls import include, path
from apps.activities.views import activity_views

app_name = "activities"
urlpatterns = [
    path(
        "submit/",
        activity_views.ActivityListCreateAPIView.as_view(),
        name="action-submit-todo",
    ),
    path("", activity_views.ActivityListCreateAPIView.as_view(), name="list-todo"),
    path(
        "<str:id>/",
        activity_views.ActivityRetrieveUpdateAPIView.as_view(),
        name="retrieve-todo",
    ),
    path(
        "<str:id>/update/",
        activity_views.ActivityRetrieveUpdateAPIView.as_view(),
        name="update-todo",
    ),
]
