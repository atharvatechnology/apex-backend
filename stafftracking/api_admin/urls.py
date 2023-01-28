from django.urls import path

from stafftracking.api_admin.views import (
    StaffTrackingListAPIView,
    StaffTrackingListPerUserAPIView,
    StaffTrackingRequestAPIView,
)

app_name = "staff-tracking"

urlpatterns = [
    path("list/", StaffTrackingListAPIView.as_view(), name="list"),
    path(
        "list/<int:user_id>/",
        StaffTrackingListPerUserAPIView.as_view(),
        name="list-user",
    ),
    path("get/<int:user_id>/", StaffTrackingRequestAPIView.as_view(), name="request"),
]
