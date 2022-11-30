from django.urls import path

from attendance.api_admin.views import (
    StudentAttendanceAdminListAPIView,
    StudentAttendanceAdminRetrieveAPIView,
    TeacherAttendanceAdminListAPIView,
    TeacherAttendanceAdminRetrieveAPIView,
)

urlpatterns = [
    path(
        "student/list/",
        StudentAttendanceAdminListAPIView.as_view(),
        name="admin-student-list",
    ),
    path(
        "student/retrieve/<int:pk>",
        StudentAttendanceAdminRetrieveAPIView.as_view(),
        name="admin-student-retrieve",
    ),
    path(
        "teacher/list/",
        TeacherAttendanceAdminListAPIView.as_view(),
        name="admin-teacher-list",
    ),
    path(
        "teacher/retrieve/<int:pk>",
        TeacherAttendanceAdminRetrieveAPIView.as_view(),
        name="admin-teacher-retrieve",
    ),
]
