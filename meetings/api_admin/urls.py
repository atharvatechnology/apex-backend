from django.urls import path

from meetings.api_admin.views import (
    MeetingCreateAPIView,
    MeetingDeleteAPIView,
    MeetingListAPIView,
    SubjectCreateAPIView,
    SubjectDeleteAPIView,
    SubjectListAPIView,
    SubjectRetrieveAPIView,
    SubjectUpdateAPIView,
)

urlpatterns = [
    path("create/", MeetingCreateAPIView.as_view(), name="meeting-create"),
    path("delete/<int:pk>/", MeetingDeleteAPIView.as_view(), name="meeting-delete"),
    path("list/<int:session_id>", MeetingListAPIView.as_view(), name="meeting-list"),
]

subject_urlpatterns = [
    path("create/", SubjectCreateAPIView.as_view(), name="subject-create"),
    path("list/", SubjectListAPIView.as_view(), name="subject-list"),
    path("retrieve/<int:pk>/", SubjectRetrieveAPIView.as_view(), name="subject-get"),
    path("delete/<int:pk>/", SubjectDeleteAPIView.as_view(), name="subject-delete"),
    path("update/<int:pk>/", SubjectUpdateAPIView.as_view(), name="subject-update"),
]
