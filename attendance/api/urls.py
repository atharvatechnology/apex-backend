from django.urls import include, path

from attendance.api.views import (
    AttendanceCreateAPIView,
    StudentAttendanceCreateAPIView,
    StudentAttendanceListAPIView,
    StudentAttendanceRetrieveAPIView,
    StudentAttendanceUpdateAPIView,
    StudentOnlineAttendanceCreateAPIView,
    TeacherAttendanceCreateAPIView,
    TeacherAttendanceListAPIView,
    TeacherAttendanceRetrieveAPIView,
    TeacherAttendanceUpdateAPIView,
)

student_urls = [
    path("list/", StudentAttendanceListAPIView.as_view(), name="attendance-list"),
    path("create/", StudentAttendanceCreateAPIView.as_view(), name="attendance-create"),
    path(
        "online/create/",
        StudentOnlineAttendanceCreateAPIView.as_view(),
        name="onlineattendance-create",
    ),
    path(
        "retrieve/<int:pk>/",
        StudentAttendanceRetrieveAPIView.as_view(),
        name="attendance-retrieve",
    ),
    path(
        "update/<int:pk>/",
        StudentAttendanceUpdateAPIView.as_view(),
        name="attendance-update",
    ),
]

teacher_urls = [
    path(
        "create/",
        TeacherAttendanceCreateAPIView.as_view(),
        name="teacher-create",
    ),
    path("list/", TeacherAttendanceListAPIView.as_view(), name="teacher-list"),
    path(
        "retrieve/<int:pk>/",
        TeacherAttendanceRetrieveAPIView.as_view(),
        name="teacher-retrieve",
    ),
    path(
        "update/<int:pk>/",
        TeacherAttendanceUpdateAPIView.as_view(),
        name="teacher-update",
    ),
]

urlpatterns = [
    path("create/", AttendanceCreateAPIView.as_view(), name="attendance-create"),
    path("student/", include(student_urls)),
    path("teacher/", include(teacher_urls)),
]
