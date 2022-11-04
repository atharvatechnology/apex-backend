from django.urls import include, path

from .views import (
    CourseSessionCreateAPIView,
    CourseSessionDeleteAPIView,
    CourseSessionListAPIView,
    CourseSessionUpdateAPIView,
    CourseThroughEnrollmentListAPIView,
    ExamEnrollmentCreateAPIView,
    ExamSessionCreateAPIView,
    ExamSessionDeleteAPIView,
    ExamSessionListAPIView,
    ExamSessionUpdateAPIView,
    ExamThroughEnrollmentListAPIView,
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
]
exam_enroll_url = [
    path(
        "create/", ExamEnrollmentCreateAPIView.as_view(), name="exam-enrollment-create"
    ),
]

course_through_enrollment_urls = [
    path(
        "list/",
        CourseThroughEnrollmentListAPIView.as_view(),
        name="course-through-enrollment-list",
    ),
]

session_urls = [
    path("exam/", include(exam_session_urls)),
    path("course/", include(course_session_urls)),
]

urlpatterns = [
    path("session/", include(session_urls)),
    path("examthroughenrollment/", include(exam_through_enrollment_urls)),
    path("coursethroughenrollment/", include(course_through_enrollment_urls)),
    path("exam-enroll/", include(exam_enroll_url)),
]
