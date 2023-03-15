from django.contrib.auth import get_user_model
from rest_framework import serializers

from stafftracking.models import StaffConnectionStatus, StaffTracking

User = get_user_model()


class StaffTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTracking
        fields = [
            "id",
            "user",
            "latitude",
            "longitude",
            "address",
            "created_at",
        ]


# class StaffTrakingRequestSerializer(serializers.Serializer):
#     user = serializers.ChoiceField(

#     )
#     class Meta:


class StaffConnectionStatusUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffConnectionStatus
        fields = [
            "is_connected",
            "is_enabled",
        ]
