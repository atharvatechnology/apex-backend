from django.urls import path

from notifications.api_admin.views import (
    NotificationAdminListAPIView,
    SendPushNotificationAdmin,
)

app_name = "notifications"

urlpatterns = [
    path("send/", SendPushNotificationAdmin.as_view(), name="send-push-notification"),
    path("list/", NotificationAdminListAPIView.as_view(), name="list"),
]
