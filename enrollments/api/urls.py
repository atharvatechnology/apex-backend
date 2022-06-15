from django.urls import path

from enrollments.api.views import (
    CourseEnrollementCreateAPIView,
    CourseEnrollementDestroyAPIView,
    CourseEnrollementListAPIView,
    CourseEnrollementRetrieveAPIView,
    CourseEnrollementUpdateAPIView,
    EnrollmentCreateAPIView,
    EnrollmentListAPIView,
    ExamEnrollmentCheckpointRetrieveAPIView,
    ExamEnrollmentRetrieveAPIView,
    ExamEnrollmentRetrievePoolAPIView,
    ExamEnrollmentUpdateAPIView,
    PhysicalBookCourseEnrollmentCreateAPIView,
    PhysicalBookCourseEnrollmentDestroyAPIView,
    PhysicalBookCourseEnrollmentListAPIView,
    PhysicalBookCourseEnrollmentRetrieveAPIView,
    PhysicalBookCourseEnrollmentUpdateAPIView,
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

urlpatterns += [
    path(
        "physical/list/",
        PhysicalBookCourseEnrollmentListAPIView.as_view(),
        name="physicalbook-list",
    ),
    path(
        "physical/create/",
        PhysicalBookCourseEnrollmentCreateAPIView.as_view(),
        name="physicalbook-create",
    ),
    path(
        "physical/update/<int:pk>/",
        PhysicalBookCourseEnrollmentUpdateAPIView.as_view(),
        name="physicalbook-create",
    ),
    path(
        "physical/retrieve/<int:pk>/",
        PhysicalBookCourseEnrollmentRetrieveAPIView.as_view(),
        name="physicalbook-retrieve",
    ),
    path(
        "physical/delete/<int:pk>/",
        PhysicalBookCourseEnrollmentDestroyAPIView.as_view(),
        name="physicalbook-destroy",
    ),
]

urlpatterns += [
    path(
        "course-enroll/list/",
        CourseEnrollementListAPIView.as_view(),
        name="course-enroll-list",
    ),
    path(
        "course-enroll/create/",
        CourseEnrollementCreateAPIView.as_view(),
        name="course-enroll-create",
    ),
    path(
        "course-enroll/update/<int:pk>/",
        CourseEnrollementUpdateAPIView.as_view(),
        name="course-enroll-update",
    ),
    path(
        "course-enroll/retrieve/<int:pk>/",
        CourseEnrollementRetrieveAPIView.as_view(),
        name="course-enroll-retrieve",
    ),
    path(
        "course-enroll/destroy/<int:pk>/",
        CourseEnrollementDestroyAPIView.as_view(),
        name="course-enroll-destroy",
    ),
]
