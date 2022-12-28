from fcm_django.models import FCMDevice
from firebase_admin.messaging import APNSConfig, APNSPayload, Aps, Message, Notification
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from common.paginations import StandardResultsSetPagination
from common.permissions import IsAdminorSuperAdminorDirector
from notifications.api_admin.serializers import NotificationAdminSerializer
from notifications.models import NotificationMessage


class SendPushNotificationAdmin(CreateAPIView):
    serializer_class = NotificationAdminSerializer
    queryset = NotificationMessage.objects.all()
    permission_classes = [IsAuthenticated & IsAdminorSuperAdminorDirector]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        data = {
            "title": serializer.data["title"],
            "body": serializer.data["body"],
        }
        message_obj = Message(
            notification=Notification(**data),
            apns=APNSConfig(
                headers={
                    "apns-priority": "5",
                },
                payload=APNSPayload(
                    aps=Aps(
                        content_available=True,
                    ),
                ),
            ),
        )
        FCMDevice.objects.all().send_message(message_obj)


class NotificationAdminListAPIView(ListAPIView):
    serializer_class = NotificationAdminSerializer
    queryset = NotificationMessage.objects.all()
    permission_classes = [IsAuthenticated & IsAdminorSuperAdminorDirector]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
