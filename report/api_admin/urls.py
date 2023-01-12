from django.urls import path

from report.api_admin.views import GeneratedReportRetrieveAPIView

app_name = "admin-report"

urlpatterns = [
    path(
        "retrieve/<int:pk>/",
        GeneratedReportRetrieveAPIView.as_view(),
        name="generated-report-retrieve",
    ),
]
