from rest_framework import serializers

from ..models import Meeting


class GenerateSignatureSerializer(serializers.Serializer):
    """Serializer for generating signature."""

    meeting_id = serializers.IntegerField()
    role = serializers.IntegerField()

    class Meta:
        fields = ("meeting_id", "role")


class MeetingOnCourseEnrolledSerializer(serializers.ModelSerializer):
    """Serializer for meeting on course enrolled."""

    class Meta:
        model = Meeting
        fields = (
            "id",
            "topic",
            "meeting_id",
            "password",
            "start_time",
            "duration",
        )
