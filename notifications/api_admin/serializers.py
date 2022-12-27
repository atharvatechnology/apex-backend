from rest_framework import serializers

from notifications.models import NotificationMessage


class NotificationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationMessage
        fields = ("title", "body", "created_at")
        read_only_fields = ("created_at",)
