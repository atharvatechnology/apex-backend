from django.urls import path

from stafftracking.api_admin.views import StaffTrackingListAPIView

urlpatterns = [
    path("list/", StaffTrackingListAPIView.as_view(), name="staff-tracking-list"),
]
