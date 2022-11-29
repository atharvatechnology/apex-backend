from django.urls import path

from attendance.api_admin.views import StudentAttendanceAdminListAPIView

urlpatterns = [
    path(
        "student/list/",
        StudentAttendanceAdminListAPIView.as_view(),
        name="admin-student-list",
    )
]
