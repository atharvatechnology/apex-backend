from rest_framework import serializers

from notifications.models import NotificationMessage


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationMessage
        fields = (
            "title",
            "body",
        )
