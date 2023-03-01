from django.urls import include, path

from .views import (
    CourseEnrollmentCreateAPIView,
    CourseGraphAPIView,
    CourseSessionCreateAPIView,
    CourseSessionDeleteAPIView,
    CourseSessionListAPIView,
    CourseSessionUpdateAPIView,
    CourseThroughEnrollmentCourseWiseListAPIView,
    CourseThroughEnrollmentGeneratorAPIView,
    CourseThroughEnrollmentListAPIView,
    CourseThroughEnrollmentListCardAPIView,
    CourseThroughEnrollmentStudentListAPIView,
    EnrollmentDeleteAdminAPIView,
    EnrollmentGraphAPIView,
    EnrollmentUpdateAdminAPIView,
    ExamEnrollmentCreateAPIView,
    ExamGraphAPIView,
    ExamResultReportGeneratorAPIView,
    ExamSessionCreateAPIView,
    ExamSessionDeleteAPIView,
    ExamSessionListAPIView,
    ExamSessionUpdateAPIView,
    ExamThroughEnrollmentGeneratorAPIView,
    ExamThroughEnrollmentListAPIView,
    ExamThroughEnrollmentListCardAPIView,
    GetCourseEnrollmentByUserAPIView,
    GetEnrollmentsByUserAPIView,
    OverallEnrollmentAPIView,
    PhysicalBookCourseEnrollmentAdminCreateAPIView,
    PhysicalBookCourseEnrollmentAdminDestroyAPIView,
    PhysicalBookCourseEnrollmentAdminListAPIView,
    PhysicalBookCourseEnrollmentAdminRetrieveAPIView,
    PhysicalBookCourseEnrollmentAdminUpdateAPIView,
    StudentCourseCheckView,
)

exam_session_urls = [
    path("create/", ExamSessionCreateAPIView.as_view(), name="exam-session-create"),
    path(
        "list/<int:exam_id>/",
        ExamSessionListAPIView.as_view(),
        name="exam-session-list",
    ),
    path(
        "update/<int:pk>/",
        ExamSessionUpdateAPIView.as_view(),
        name="exam-session-update",
    ),
    path(
        "delete/<int:pk>/",
        ExamSessionDeleteAPIView.as_view(),
        name="exam-session-delete",
    ),
]

exam_graph = [path("bar/", ExamGraphAPIView.as_view(), name="exam-graph")]

course_graph = [
    path("bar/", CourseGraphAPIView.as_view(), name="exam-graph"),
    path("donut/", EnrollmentGraphAPIView.as_view(), name="enroll-graph"),
    path("overall/", OverallEnrollmentAPIView.as_view(), name="overall-enroll"),
]

course_session_urls = [
    path("create/", CourseSessionCreateAPIView.as_view(), name="course-session-create"),
    path(
        "list/<int:course_id>/",
        CourseSessionListAPIView.as_view(),
        name="course-session-list",
    ),
    path(
        "update/<int:pk>/",
        CourseSessionUpdateAPIView.as_view(),
        name="course-session-update",
    ),
    path(
        "delete/<int:pk>/",
        CourseSessionDeleteAPIView.as_view(),
        name="course-session-delete",
    ),
    path(
        "check/",
        StudentCourseCheckView.as_view(),
        name="student-course-check",
    ),
]

exam_through_enrollment_urls = [
    path(
        "list/",
        ExamThroughEnrollmentListAPIView.as_view(),
        name="exam-through-enrollment-list",
    ),
    path(
        "report/generate/",
        ExamThroughEnrollmentGeneratorAPIView.as_view(),
        name="generator-enrollment",
    ),
    path(
        "card/",
        ExamThroughEnrollmentListCardAPIView.as_view(),
        name="exam-through-enrollment-card",
    ),
    path(
        "result/report/generate/",
        ExamResultReportGeneratorAPIView.as_view(),
        name="generator-exam-result",
    ),
]

exam_enroll_url = [
    path(
        "create/", ExamEnrollmentCreateAPIView.as_view(), name="exam-enrollment-create"
    ),
]

course_enroll_url = [
    path(
        "create/",
        CourseEnrollmentCreateAPIView.as_view(),
        name="course-enrollment-create",
    ),
]

course_through_enrollment_urls = [
    path(
        "detail/<int:course_id>/",
        CourseThroughEnrollmentCourseWiseListAPIView.as_view(),
        name="detail",
    ),
    path(
        "list/",
        CourseThroughEnrollmentListAPIView.as_view(),
        name="course-through-enrollment-list",
    ),
    path(
        "student/<int:student_id>/",
        CourseThroughEnrollmentStudentListAPIView.as_view(),
        name="course-through-enrollment-list",
    ),
    path(
        "card/",
        CourseThroughEnrollmentListCardAPIView.as_view(),
        name="course-through-enrollment-card",
    ),
    path(
        "report/generate/",
        CourseThroughEnrollmentGeneratorAPIView.as_view(),
        name="generator-course",
    ),
]

session_urls = [
    path("exam/", include(exam_session_urls)),
    path("course/", include(course_session_urls)),
]

enrollment_urls = [
    path(
        "get-by-user/<str:student_code>/",
        GetCourseEnrollmentByUserAPIView.as_view(),
        name="get-enrollment_by_user",
    ),
    path(
        "user/<str:student_id>/",
        GetEnrollmentsByUserAPIView.as_view(),
        name="get-enrollments_by_user",
    ),
    path(
        "delete/<int:pk>/",
        EnrollmentDeleteAdminAPIView.as_view(),
        name="enrollment-delete-admin",
    ),
    path(
        "update/<int:pk>/",
        EnrollmentUpdateAdminAPIView.as_view(),
        name="enrollment-update-admin",
    ),
]

physical_urls = [
    path(
        "list/",
        PhysicalBookCourseEnrollmentAdminListAPIView.as_view(),
        name="physicalbook-admin-list",
    ),
    path(
        "create/",
        PhysicalBookCourseEnrollmentAdminCreateAPIView.as_view(),
        name="physicalbook-admin-create",
    ),
    path(
        "update/<int:pk>/",
        PhysicalBookCourseEnrollmentAdminUpdateAPIView.as_view(),
        name="physicalbook-admin-update",
    ),
    path(
        "retrieve/<int:pk>/",
        PhysicalBookCourseEnrollmentAdminRetrieveAPIView.as_view(),
        name="physicalbook-admin-retrieve",
    ),
    path(
        "delete/<int:pk>/",
        PhysicalBookCourseEnrollmentAdminDestroyAPIView.as_view(),
        name="physicalbook-admin-destroy",
    ),
]

urlpatterns = [
    path("", include(enrollment_urls)),
    path("exam-graph/", include(exam_graph)),
    path("course-graph/", include(course_graph)),
    path("session/", include(session_urls)),
    path("examthroughenrollment/", include(exam_through_enrollment_urls)),
    path("coursethroughenrollment/", include(course_through_enrollment_urls)),
    path("exam-enroll/", include(exam_enroll_url)),
    path("course-enroll/", include(course_enroll_url)),
    path("physical/", include(physical_urls)),
]
