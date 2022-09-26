from rest_framework import serializers

from ..models import Meeting, Subject


class GenerateSignatureSerializer(serializers.Serializer):
    """Serializer for generating signature."""

    meeting_id = serializers.IntegerField()
    role = serializers.IntegerField()

    class Meta:
        fields = ("meeting_id", "role")


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for subject on meeting retrieval."""

    class Meta:
        model = Subject
        fields = ("id", "name")


class MeetingOnCourseEnrolledSerializer(serializers.ModelSerializer):
    """Serializer for meeting on course enrolled."""

    subject = SubjectSerializer()

    class Meta:
        model = Meeting
        fields = (
            "id",
            "topic",
            "meeting_id",
            "password",
            "start_time",
            "duration",
            "subject",
        )
