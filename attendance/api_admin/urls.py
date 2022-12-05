from django.urls import include, path

from attendance.api_admin.views import (
    StudentAttendanceAdminDeleteAPIView,
    StudentAttendanceAdminHistoryListAPIView,
    StudentAttendanceAdminListAPIView,
    StudentAttendanceAdminRetrieveAPIView,
    StudentAttendanceAdminUpdateAPIView,
    TeacherAttendanceAdminDeleteAPIView,
    TeacherAttendanceAdminHistoryListAPIView,
    TeacherAttendanceAdminListAPIView,
    TeacherAttendanceAdminRetrieveAPIView,
    TeacherAttendanceAdminUpdateAPIView,
    TeacherAttendanceDetailAdminDeleteAPIView,
    TeacherAttendanceDetailAdminHistoryListAPIView,
    TeacherAttendanceDetailAdminListAPIView,
    TeacherAttendanceDetailAdminRetrieveAPIView,
    TeacherAttendanceDetailAdminUpdateAPIView,
)

student_admin_urls = [
    path(
        "student/list/",
        StudentAttendanceAdminListAPIView.as_view(),
        name="admin-student-list",
    ),
    path(
        "student/history/list/<int:student_id>",
        StudentAttendanceAdminHistoryListAPIView.as_view(),
        name="admin-student-history-list",
    ),
    path(
        "student/retrieve/<int:pk>",
        StudentAttendanceAdminRetrieveAPIView.as_view(),
        name="admin-student-retrieve",
    ),
    path(
        "student/update/<int:pk>",
        StudentAttendanceAdminUpdateAPIView.as_view(),
        name="admin-student-update",
    ),
    path(
        "student/delete/<int:pk>",
        StudentAttendanceAdminDeleteAPIView.as_view(),
        name="admin-student-delete",
    ),
]

teacher_admin_urls = [
    path(
        "teacher/list/",
        TeacherAttendanceAdminListAPIView.as_view(),
        name="admin-teacher-list",
    ),
    path(
        "teacher/history/list/<int:teacher_id>",
        TeacherAttendanceAdminHistoryListAPIView.as_view(),
        name="admin-teacher-history-list",
    ),
    path(
        "teacher/retrieve/<int:pk>",
        TeacherAttendanceAdminRetrieveAPIView.as_view(),
        name="admin-teacher-retrieve",
    ),
    path(
        "teacher/update/<int:pk>",
        TeacherAttendanceAdminUpdateAPIView.as_view(),
        name="admin-teacher-update",
    ),
    path(
        "teacher/delete/<int:pk>",
        TeacherAttendanceAdminDeleteAPIView.as_view(),
        name="admin-teacher-delete",
    ),
    path(
        "teacher/detail/list/",
        TeacherAttendanceDetailAdminListAPIView.as_view(),
        name="admin-teacher-detail-list",
    ),
    path(
        "teacher/detail/history/list/<int:teacher_detail_id>",
        TeacherAttendanceDetailAdminHistoryListAPIView.as_view(),
        name="admin-teacher-detail-history-list",
    ),
    path(
        "teacher/detail/retrieve/<int:pk>",
        TeacherAttendanceDetailAdminRetrieveAPIView.as_view(),
        name="admin-teacher-detail-retrieve",
    ),
    path(
        "teacher/detail/update/<int:pk>",
        TeacherAttendanceDetailAdminUpdateAPIView.as_view(),
        name="admin-teacher-detail-update",
    ),
    path(
        "teacher/detail/delete/<int:pk>",
        TeacherAttendanceDetailAdminDeleteAPIView.as_view(),
        name="admin-teacher-detail-delete",
    ),
]


urlpatterns = [
    path("student/", include(student_admin_urls)),
    path("teacher/", include(teacher_admin_urls)),
]
