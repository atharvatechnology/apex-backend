from django.urls import include, path

from dashboard.api_admin.views import (
    DashboardAttendanceAPIView,
    DashboardEnrollmentCourseCategoryAPIView,
    DashboardEnrollmentExamCountAPIView,
    DashboardEnrollmentOverallCourseAPIView,
    DashboardOverviewAPIView,
    DashboardRevenueCourseAPIView,
    DashboardRevenueGraphAPIView,
    DashboardRevenueOverviewAPIView,
)

app_name = "dashboard.api.admin"

revenue_urlpatterns = [
    path(
        "overview/",
        DashboardRevenueOverviewAPIView.as_view(),
        name="overview",
    ),
    path("graph/<int:year>/", DashboardRevenueGraphAPIView.as_view(), name="graph"),
    path("courses/<int:year>/", DashboardRevenueCourseAPIView.as_view(), name="course"),
]

enrollment_urlpatterns = [
    path(
        "course/overview/<int:year>/", DashboardEnrollmentOverallCourseAPIView.as_view()
    ),
    path(
        "course/category/<int:year>/",
        DashboardEnrollmentCourseCategoryAPIView.as_view(),
    ),
    path("exam/", DashboardEnrollmentExamCountAPIView.as_view(), name="exam-get"),
]

attendance_urlpatterns = [
    path("get/", DashboardAttendanceAPIView.as_view(), name="attendance-get"),
]


urlpatterns = [
    path("overview/", DashboardOverviewAPIView.as_view(), name="overview"),
    path("revenue/", include(revenue_urlpatterns)),
    path("enrollment/", include(enrollment_urlpatterns)),
    path("attendance/", include(attendance_urlpatterns)),
]
