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
    is_joinable = serializers.SerializerMethodField()

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
            "is_joinable",
        )

    def get_is_joinable(self, obj):
        return obj.is_joinable


class MeetingSerializer(serializers.ModelSerializer):
    """Base meeting serializer."""

    class Meta:
        model = Meeting
        fields = (
            "id",
            "topic",
            "meeting_id",
            # "type",
            "start_time",
            "password",
            # "agenda",
            "duration",
            "course_session",
            "subject",
            "variant",
            "end_date_time",
            "repeat_type",
            "repeat_interval",
            "monthly_day",
            "weekly_days",
        )
        read_only_fields = ("id", "meeting_id")


class MeetingCourseSessionSerializer(serializers.ModelSerializer):
    """Meeting Course Session serializer."""

    class Meta:
        model = Meeting
        fields = ("course_session",)
