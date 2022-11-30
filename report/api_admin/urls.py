from django.urls import path

from report.api_admin.views import GeneratedReportListAPIView

app_name = "admin-report"

urlpatterns = [
    path("list/", GeneratedReportListAPIView.as_view(), name="generated-report-list"),
]
