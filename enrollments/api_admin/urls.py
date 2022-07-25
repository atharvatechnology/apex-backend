from django.urls import include, path

from .views import (
    ExamEnrollmentCreateAPIView,
    ExamThroughEnrollmentListAPIView,
    SessionCreateAPIView,
    SessionDeleteAPIView,
    SessionListAPIView,
    SessionUpdateAPIView,
)

session_urls = [
    path("create/", SessionCreateAPIView.as_view(), name="session-create"),
    path("list/<int:exam_id>/", SessionListAPIView.as_view(), name="session-list"),
    path("update/<int:pk>/", SessionUpdateAPIView.as_view(), name="session-update"),
    path("delete/<int:pk>/", SessionDeleteAPIView.as_view(), name="session-delete"),
]
exam_through_enrollment_urls = [
    path(
        "list/",
        ExamThroughEnrollmentListAPIView.as_view(),
        name="exam-through-enrollment-list",
    ),
]
exam_enroll_url = [
    path(
        "create/", ExamEnrollmentCreateAPIView.as_view(), name="exam-enrollment-create"
    ),
]


urlpatterns = [
    path("session/", include(session_urls)),
    path("examthroughenrollment/", include(exam_through_enrollment_urls)),
    path("exam-enroll/", include(exam_enroll_url)),
]
