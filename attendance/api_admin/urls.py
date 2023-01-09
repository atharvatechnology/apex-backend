from django.urls import include, path

from attendance.api_admin.views import (
    StudentAttendanceAdminDeleteAPIView,
    StudentAttendanceAdminHistoryListAPIView,
    StudentAttendanceAdminListAPIView,
    StudentAttendanceAdminRetrieveAPIView,
    StudentAttendanceAdminUpdateAPIView,
    StudentAttendanceReportGeneratorAPIView,
    TeacherAttendanceAdminDeleteAPIView,
    TeacherAttendanceAdminHistoryListAPIView,
    TeacherAttendanceAdminListAPIView,
    TeacherAttendanceAdminRetrieveAPIView,
    TeacherAttendanceAdminUpdateAPIView,
    TeacherAttendanceDetailAdminDeleteAPIView,
    TeacherAttendanceDetailAdminListAPIView,
    TeacherAttendanceDetailAdminRetrieveAPIView,
    TeacherAttendanceDetailAdminUpdateAPIView,
    TeacherAttendanceReportGeneratorAPIView,
)

student_admin_urls = [
    path(
        "list/",
        StudentAttendanceAdminListAPIView.as_view(),
        name="admin-student-list",
    ),
    path(
        "history/list/<int:student_id>/",
        StudentAttendanceAdminHistoryListAPIView.as_view(),
        name="admin-student-history-list",
    ),
    path(
        "retrieve/<int:pk>/",
        StudentAttendanceAdminRetrieveAPIView.as_view(),
        name="admin-student-retrieve",
    ),
    path(
        "update/<int:pk>/",
        StudentAttendanceAdminUpdateAPIView.as_view(),
        name="admin-student-update",
    ),
    path(
        "delete/<int:pk>/",
        StudentAttendanceAdminDeleteAPIView.as_view(),
        name="admin-student-delete",
    ),
    path(
        "report/generate/",
        StudentAttendanceReportGeneratorAPIView.as_view(),
        name="generator-student-attendance",
    ),
]


teacher_admin_details_urls = [
    path(
        "list/<int:attendance_id>/",
        TeacherAttendanceDetailAdminListAPIView.as_view(),
        name="admin-teacher-detail-list",
    ),
    path(
        "retrieve/<int:pk>/",
        TeacherAttendanceDetailAdminRetrieveAPIView.as_view(),
        name="admin-teacher-detail-retrieve",
    ),
    path(
        "update/<int:pk>/",
        TeacherAttendanceDetailAdminUpdateAPIView.as_view(),
        name="admin-teacher-detail-update",
    ),
    path(
        "delete/<int:pk>/",
        TeacherAttendanceDetailAdminDeleteAPIView.as_view(),
        name="admin-teacher-detail-delete",
    ),
]


teacher_admin_urls = [
    path(
        "list/",
        TeacherAttendanceAdminListAPIView.as_view(),
        name="admin-teacher-list",
    ),
    path(
        "history/list/<int:teacher_id>/",
        TeacherAttendanceAdminHistoryListAPIView.as_view(),
        name="admin-teacher-history-list",
    ),
    path(
        "retrieve/<int:pk>/",
        TeacherAttendanceAdminRetrieveAPIView.as_view(),
        name="admin-teacher-retrieve",
    ),
    path(
        "update/<int:pk>/",
        TeacherAttendanceAdminUpdateAPIView.as_view(),
        name="admin-teacher-update",
    ),
    path(
        "delete/<int:pk>/",
        TeacherAttendanceAdminDeleteAPIView.as_view(),
        name="admin-teacher-delete",
    ),
    path(
        "detail/",
        include(teacher_admin_details_urls),
    ),
    path(
        "report/generate/",
        TeacherAttendanceReportGeneratorAPIView.as_view(),
        name="generator-teacher-attendance",
    ),
]

urlpatterns = [
    path("student/", include(student_admin_urls)),
    path("teacher/", include(teacher_admin_urls)),
]
