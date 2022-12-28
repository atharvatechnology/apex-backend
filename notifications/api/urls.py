from django.urls import path

from notifications.api.views import NotificationListAPIView

app_name = "api.notifications"

urlpatterns = [
    path("list/", NotificationListAPIView.as_view(), name="list"),
]
