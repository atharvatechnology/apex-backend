from django.urls import path

from enrollments.api.views import (
    EnrollmentCreateAPIView,
    EnrollmentListAPIView,
    ExamEnrollmentCheckpointRetrieveAPIView,
    ExamEnrollmentRetrieveAPIView,
    ExamEnrollmentRetrievePoolAPIView,
    ExamEnrollmentUpdateAPIView,
    SessionCreateAPIView,
)

urlpatterns = [
    path("session/create/", SessionCreateAPIView.as_view(), name="session-create"),
]

urlpatterns += [
    path("create/", EnrollmentCreateAPIView.as_view(), name="enrollment-create"),
    path("list/", EnrollmentListAPIView.as_view(), name="enrollment-list"),
]

urlpatterns += [
    path(
        "exam/submit/<int:pk>",
        ExamEnrollmentUpdateAPIView.as_view(),
        name="exam-enrollment-submit",
    ),
    path(
        "exam/result/<int:pk>",
        ExamEnrollmentRetrieveAPIView.as_view(),
        name="exam-enrollment-result",
    ),
    path(
        "exam/result/<int:pk>/pool/",
        ExamEnrollmentRetrievePoolAPIView.as_view(),
        name="exam-enrollment-result",
    ),
    path(
        "exam/checkpoint/<int:pk>",
        ExamEnrollmentCheckpointRetrieveAPIView.as_view(),
        name="exam-enrollment-checkpoint",
    ),
]
