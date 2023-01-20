from django.contrib.auth import get_user_model
from rest_framework import serializers

from stafftracking.models import StaffTracking

User = get_user_model()


class StaffTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTracking
        fields = [
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
