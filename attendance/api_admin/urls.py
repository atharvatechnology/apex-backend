from django.urls import path

from attendance.api_admin.views import (
    StudentAttendanceAdminListAPIView,
    TeacherAttendanceAdminListAPIView,
)

urlpatterns = [
    path(
        "student/list/",
        StudentAttendanceAdminListAPIView.as_view(),
        name="admin-student-list",
    ),
    path(
        "teacher/list/",
        TeacherAttendanceAdminListAPIView.as_view(),
        name="admin-teacher-list",
    ),
]
