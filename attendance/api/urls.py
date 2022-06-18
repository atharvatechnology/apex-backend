from django.urls import path

from attendance.api.views import (
    AttendanceCreateAPIView,
    AttendanceDeleteAPIView,
    AttendanceListAPIView,
    AttendanceRetrieveAPIView,
    AttendanceUpdateAPIView,
    TeacherAttendanceCreateAPIView,
    TeacherAttendanceDeleteAPIView,
    TeacherAttendanceListAPIView,
    TeacherAttendanceRetrieveAPIView,
    TeacherAttendanceUpdateAPIView,
)

urlpatterns = [
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
    path(
        "delete/<int:pk>/", AttendanceDeleteAPIView.as_view(), name="attendance-delete"
    ),
    path(
        "teacher/create/",
        TeacherAttendanceCreateAPIView.as_view(),
        name="teacher-create",
    ),
    path("teacher/list/", TeacherAttendanceListAPIView.as_view(), name="teacher-list"),
    path(
        "teacher/<int:pk>/",
        TeacherAttendanceRetrieveAPIView.as_view(),
        name="teacher-retrieve",
    ),
    path(
        "teacher/update/<int:pk>/",
        TeacherAttendanceUpdateAPIView.as_view(),
        name="teacher-update",
    ),
    path(
        "teacher/delete/<int:pk>/",
        TeacherAttendanceDeleteAPIView.as_view(),
        name="teacher-delete",
    ),
]
