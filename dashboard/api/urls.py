from django.urls import path

from dashboard.api.views import DashboardViewCountAPIView

app_name = "dashboard.api"

urlpatterns = [path("get/", DashboardViewCountAPIView.as_view(), name="get")]
