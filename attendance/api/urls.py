from django.urls import path

from attendance.api.views import (  # TeacherAttendanceRetrieveAPIView,
    AttendanceCreateAPIView,
    AttendanceDeleteAPIView,
    AttendanceListAPIView,
    AttendanceRetrieveAPIView,
    AttendanceUpdateAPIView,
    TeacherAttendanceCreateAPIView,
    TeacherAttendanceDetailDeleteAPIView,
    TeacherAttendanceDetailListAPIView,
    TeacherAttendanceDetailRetrieveAPIView,
    TeacherAttendanceDetailUpdateAPIView,
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
    path(
        "teacher/detail/list/",
        TeacherAttendanceDetailListAPIView.as_view(),
        name="teacher-detail-list",
    ),
    path(
        "teacher/detail/<int:pk>/",
        TeacherAttendanceDetailRetrieveAPIView.as_view(),
        name="teacher-detail-retrieve",
    ),
    path(
        "teacher/detail/update/<int:pk>/",
        TeacherAttendanceDetailUpdateAPIView.as_view(),
        name="teacher-detail-update",
    ),
    path(
        "teacher/detail/delete/<int:pk>/",
        TeacherAttendanceDetailDeleteAPIView.as_view(),
        name="teacher-detail-delete",
    ),
]
