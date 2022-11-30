from django.urls import include, path

from dashboard.api_admin.views import (
    DashboardOverviewAPIView,
    DashboardRevenueCourseAPIView,
    DashboardRevenueGraphAPIView,
    DashboardRevenueOverviewAPIView,
)

app_name = "dashboard.api.admin"

revenue_urlpatterns = [
    path(
        "overview/<int:year>/",
        DashboardRevenueOverviewAPIView.as_view(),
        name="overview",
    ),
    path("graph/<int:year>/", DashboardRevenueGraphAPIView.as_view(), name="graph"),
    path("courses/<int:year>/", DashboardRevenueCourseAPIView.as_view(), name="course"),
]


urlpatterns = [
    path("overview/", DashboardOverviewAPIView.as_view(), name="overview"),
    path("revenue/", include(revenue_urlpatterns)),
]
