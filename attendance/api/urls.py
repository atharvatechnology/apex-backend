from django.urls import include, path

from attendance.api.views import (
    AttendanceCreateAPIView,
    AttendanceListAPIView,
    AttendanceRetrieveAPIView,
    AttendanceUpdateAPIView,
    TeacherAttendanceCreateAPIView,
    TeacherAttendanceListAPIView,
    TeacherAttendanceRetrieveAPIView,
    TeacherAttendanceUpdateAPIView,
)

student_urls = [
    path("list/", AttendanceListAPIView.as_view(), name="attendance-list"),
    path("create/", AttendanceCreateAPIView.as_view(), name="attendance-create"),
    path(
        "retrieve/<int:pk>/",
        AttendanceRetrieveAPIView.as_view(),
        name="attendance-retrieve",
    ),
    path(
        "update/<int:pk>/", AttendanceUpdateAPIView.as_view(), name="attendance-update"
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
    path("student/", include(student_urls)),
    path("teacher/", include(teacher_urls)),
]