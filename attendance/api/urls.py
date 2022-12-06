from django.urls import include, path

from attendance.api.views import (
    AttendanceCreateAPIView,
    StudentAttendanceCreateAPIView,
    StudentAttendanceListAPIView,
    StudentAttendanceRetrieveAPIView,
    StudentOnlineAttendanceCreateAPIView,
    TeacherAttendanceCreateAPIView,
    TeacherAttendanceDetailCreateAPIView,
    TeacherAttendanceDetailListAPIView,
    TeacherAttendanceDetailRetrieveAPIView,
    TeacherAttendanceDetailUpdateAPIView,
    TeacherAttendanceListAPIView,
    TeacherAttendanceRetrieveAPIView,
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
        "create/detail/",
        TeacherAttendanceDetailCreateAPIView.as_view(),
        name="teacher-detail-create",
    ),
    path(
        "list/detail/<int:teacher_attendance_id>",
        TeacherAttendanceDetailListAPIView.as_view(),
        name="teacher-detail-list",
    ),
    path(
        "retrieve/detail/<int:pk>/",
        TeacherAttendanceDetailRetrieveAPIView.as_view(),
        name="teacher-detail-retrieve",
    ),
    path(
        "update/detail/<int:pk>/",
        TeacherAttendanceDetailUpdateAPIView.as_view(),
        name="teacher-detail-update",
    ),
]

urlpatterns = [
    path("create/", AttendanceCreateAPIView.as_view(), name="attendance-create"),
    path("student/", include(student_urls)),
    path("teacher/", include(teacher_urls)),
]
