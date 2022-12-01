from django.urls import path

from attendance.api_admin.views import (
    StudentAttendanceAdminListAPIView,
    TeacherAttendanceAdminListAPIView,
)

urlpatterns = [
    path(
        "student/list/<int:student_id>",
        StudentAttendanceAdminListAPIView.as_view(),
        name="admin-student-list",
    ),
    # path(
    #     "student/retrieve/<int:pk>",
    #     StudentAttendanceAdminRetrieveAPIView.as_view(),
    #     name="admin-student-retrieve",
    # ),
    path(
        "teacher/list/<int:teacher_id>",
        TeacherAttendanceAdminListAPIView.as_view(),
        name="admin-teacher-list",
    ),
    # path(
    #     "teacher/retrieve/<int:pk>",
    #     TeacherAttendanceAdminRetrieveAPIView.as_view(),
    #     name="admin-teacher-retrieve",
    # ),
]
