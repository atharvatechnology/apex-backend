from django.urls import path

from meetings.api_admin.views import MeetingCreateAPIView, MeetingDeleteAPIView

urlpatterns = [
    path("create/", MeetingCreateAPIView.as_view(), name="meeting-create"),
    path("delete/<int:pk>/", MeetingDeleteAPIView.as_view(), name="meeting-delete"),
]
