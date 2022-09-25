from django.urls import path

from notifications.api_admin.views import SendPushNotification

urlpatterns = [
    path("", SendPushNotification.as_view(), name="send-push-notification"),
]
