from django.urls import include, path

from .views import (
    SessionCreateAPIView,
    SessionDeleteAPIView,
    SessionListAPIView,
    SessionUpdateAPIView,
    ExamThroughEnrollmentListAPIView
)

session_urls = [
    path("create/", SessionCreateAPIView.as_view(), name="session-create"),
    path("list/<int:exam_id>/", SessionListAPIView.as_view(), name="session-list"),
    path("update/<int:pk>/", SessionUpdateAPIView.as_view(), name="session-update"),
    path("delete/<int:pk>/", SessionDeleteAPIView.as_view(), name="session-delete"),
]
exam_through_enrollment_urls = [
    path("list/", ExamThroughEnrollmentListAPIView.as_view(), name="exam-through-enrollment-list"),
]

urlpatterns = [
    path("session/", include(session_urls)),
    path("examthroughenrollment/", include(exam_through_enrollment_urls)),

]
