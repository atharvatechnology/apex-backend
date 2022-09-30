from django.urls import path

from notifications.api_admin.views import NotificationListAPIView, SendPushNotification

app_name = "notifications"

urlpatterns = [
    path("send/", SendPushNotification.as_view(), name="send-push-notification"),
    path("list/", NotificationListAPIView.as_view(), name="list"),
]
