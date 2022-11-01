from django.urls import include, path

from enrollments.api.views import (
    CheckIfStudentInCourse,
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
    ExamThroughEnrollmentGeneratorAPIView,
    PhysicalBookCourseEnrollmentCreateAPIView,
    PhysicalBookCourseEnrollmentDestroyAPIView,
    PhysicalBookCourseEnrollmentListAPIView,
    PhysicalBookCourseEnrollmentRetrieveAPIView,
    PhysicalBookCourseEnrollmentUpdateAPIView,
)

enrollment_urls = [
    path("create/", EnrollmentCreateAPIView.as_view(), name="enrollment-create"),
    path("list/", EnrollmentListAPIView.as_view(), name="enrollment-list"),
    path(
        "generator/list/",
        ExamThroughEnrollmentGeneratorAPIView.as_view(),
        name="generator-enrollment",
    ),
]

exam_urls = [
    path(
        "submit/<int:pk>",
        ExamEnrollmentUpdateAPIView.as_view(),
        name="exam-enrollment-submit",
    ),
    path(
        "result/<int:pk>",
        ExamEnrollmentRetrieveAPIView.as_view(),
        name="exam-enrollment-result",
    ),
    path(
        "result/<int:pk>/pool/",
        ExamEnrollmentRetrievePoolAPIView.as_view(),
        name="exam-enrollment-result",
    ),
    path(
        "checkpoint/<int:pk>",
        ExamEnrollmentCheckpointRetrieveAPIView.as_view(),
        name="exam-enrollment-checkpoint",
    ),
]

physical_urls = [
    path(
        "list/",
        PhysicalBookCourseEnrollmentListAPIView.as_view(),
        name="physicalbook-list",
    ),
    path(
        "create/",
        PhysicalBookCourseEnrollmentCreateAPIView.as_view(),
        name="physicalbook-create",
    ),
    path(
        "update/<int:pk>/",
        PhysicalBookCourseEnrollmentUpdateAPIView.as_view(),
        name="physicalbook-create",
    ),
    path(
        "retrieve/<int:pk>/",
        PhysicalBookCourseEnrollmentRetrieveAPIView.as_view(),
        name="physicalbook-retrieve",
    ),
    path(
        "delete/<int:pk>/",
        PhysicalBookCourseEnrollmentDestroyAPIView.as_view(),
        name="physicalbook-destroy",
    ),
]

course_enroll_urls = [
    path(
        "list/",
        CourseEnrollementListAPIView.as_view(),
        name="course-enroll-list",
    ),
    path(
        "update/<int:pk>/",
        CourseEnrollementUpdateAPIView.as_view(),
        name="course-enroll-update",
    ),
    path(
        "retrieve/<int:pk>/",
        CourseEnrollementRetrieveAPIView.as_view(),
        name="course-enroll-retrieve",
    ),
    path(
        "destroy/<int:pk>/",
        CourseEnrollementDestroyAPIView.as_view(),
        name="course-enroll-destroy",
    ),
]

check_enroll_urls = [
    path("student-enroll/", CheckIfStudentInCourse.as_view(), name="stu-enroll"),
]

urlpatterns = [
    path("", include(enrollment_urls)),
    path("exam/", include(exam_urls)),
    path("physical/", include(physical_urls)),
    path("course-enroll/", include(course_enroll_urls)),
    path("check/", include(check_enroll_urls)),
    # path("dynamic/", dynamic_excel_generator,)
]
