from django.urls import include, path

from .views import (
    CourseEnrollmentCreateAPIView,
    CourseGeneratorAPIView,
    CourseGraphAPIView,
    CourseSessionCreateAPIView,
    CourseSessionDeleteAPIView,
    CourseSessionListAPIView,
    CourseSessionUpdateAPIView,
    CourseThroughEnrollmentGeneratorAPIView,
    CourseThroughEnrollmentListAPIView,
    EnrollmentDeleteAdminAPIView,
    EnrollmentGraphAPIView,
    EnrollmentUpdateAdminAPIView,
    ExamEnrollmentCreateAPIView,
    ExamGeneratorAPIView,
    ExamGraphAPIView,
    ExamSessionCreateAPIView,
    ExamSessionDeleteAPIView,
    ExamSessionListAPIView,
    ExamSessionUpdateAPIView,
    ExamThroughEnrollmentGeneratorAPIView,
    ExamThroughEnrollmentListAPIView,
    OverallEnrollmentAPIView,
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
    path(
        "report/generate/",
        ExamGeneratorAPIView.as_view(),
        name="generator-exam-sessions",
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
    path(
        "report/generate/",
        CourseGeneratorAPIView.as_view(),
        name="generator-course-sessions",
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
        "list/",
        CourseThroughEnrollmentListAPIView.as_view(),
        name="course-through-enrollment-list",
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
        "delete/",
        EnrollmentDeleteAdminAPIView.as_view(),
        name="enrollment-delete-admin",
    ),
    path(
        "update/",
        EnrollmentUpdateAdminAPIView.as_view(),
        name="enrollment-update-admin",
    ),
]

urlpatterns = [
    path("exam-graph/", include(exam_graph)),
    path("course-graph/", include(course_graph)),
    path("session/", include(session_urls)),
    path("examthroughenrollment/", include(exam_through_enrollment_urls)),
    path("coursethroughenrollment/", include(course_through_enrollment_urls)),
    path("exam-enroll/", include(exam_enroll_url)),
    path("course-enroll/", include(course_enroll_url)),
]
