from rest_framework import serializers

from meetings.providers.register import provider_factory

from ..models import Meeting


class MeetingCreateSerializer(serializers.ModelSerializer):
    """Serializer when admin is creating a meeting."""

    class Meta:
        model = Meeting
        fields = (
            "id",
            "topic",
            # "type",
            "start_time",
            "password",
            # "agenda",
            "duration",
            "course",
            "subject",
            "variant",
        )

    def create(self, validated_data):
        """Create a meeting."""
        variant = validated_data.get("variant")
        duration = validated_data.get("duration")
        start_time = validated_data.get("start_time")
        duration_in_minutes = duration.total_seconds() / 60.0

        meeting_provider = provider_factory.get_provider(
            variant, name=f"{variant} meeting"
        )
        meeting_config = {
            "title": validated_data.get("topic"),
            "duration": int(duration_in_minutes),
            "password": validated_data.get("password"),
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        meeting_details = meeting_provider.create_meeting(meeting_config)
        meeting_instance = Meeting(
            variant=variant,
            course=validated_data.get("course"),
            subject=validated_data.get("subject"),
            meeting_id=meeting_details.get("id"),
            host_id=meeting_details.get("host_id"),
            host_email=meeting_details.get("host_email"),
            topic=meeting_details.get("topic"),
            meeting_type=meeting_details.get("type"),
            occurence_status=meeting_details.get("status"),
            start_time=start_time,
            password=meeting_details.get("password"),
            created_at=meeting_details.get("created_at"),
            agenda=meeting_details.get("agenda"),
            duration=duration,
        )
        meeting_instance.save()
        return meeting_instance
