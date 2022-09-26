import pytz
from rest_framework import serializers

from meetings.providers.register import provider_factory

from ..models import Meeting, Subject


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


class MeetingCreateSerializer(MeetingSerializer):
    """Serializer when admin is creating a meeting."""

    class Meta:
        model = Meeting
        fields = MeetingSerializer.Meta.fields
        read_only_fields = MeetingSerializer.Meta.read_only_fields

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        repeat_type = validated_data.get(
            "repeat_type", Meeting.repeat_type.field.default
        )
        repeat_interval = validated_data.get(
            "repeat_interval",
            Meeting.repeat_interval.field.default,
        )
        monthly_day = validated_data.get("monthly_day")
        weekly_days = validated_data.get("weekly_days")
        if repeat_type == 3:
            if not monthly_day:
                raise serializers.ValidationError(
                    f"Repeat type {repeat_type} can't have "
                    + f"monthly_day value {monthly_day}."
                )
            if repeat_interval > 3:
                raise serializers.ValidationError(
                    f"Repeat interval {repeat_interval} can't be greater than 3 months."
                )
        elif repeat_type == 2:
            if not weekly_days:
                raise serializers.ValidationError(
                    f"Repeat type {repeat_type} can't"
                    + f"have weekly_days value {weekly_days}."
                )
            weekly_days_set = {int(s_int) for s_int in weekly_days.split(",")}
            seven_day_set = set(range(1, 8))
            if not weekly_days_set.issubset(seven_day_set):
                raise serializers.ValidationError(
                    f"Repeat type {repeat_type} can't have "
                    + f"weekly_days value {weekly_days}."
                )
            if repeat_interval > 12:
                raise serializers.ValidationError(
                    f"Repeat interval {repeat_interval} can't be greater than 12 weeks."
                )
        elif repeat_type == 1:
            if repeat_interval > 90:
                raise serializers.ValidationError(
                    f"Repeat interval {repeat_interval} can't be greater than 90 days."
                )
        return validated_data

    def create(self, validated_data):
        """Create a meeting."""
        variant = validated_data.get("variant", "zoom")
        duration = validated_data.get("duration")
        start_time = validated_data.get("start_time")
        end_date_time = validated_data.get("end_date_time")
        repeat_type = validated_data.get(
            "repeat_type", Meeting.repeat_type.field.default
        )
        repeat_interval = validated_data.get(
            "repeat_interval",
            Meeting.repeat_interval.field.default,
        )
        monthly_day = validated_data.get("monthly_day")
        weekly_days = validated_data.get("weekly_days")
        duration_in_minutes = duration.total_seconds() / 60.0

        meeting_provider = provider_factory.get_provider(variant)
        meeting_config = {
            "title": validated_data.get("topic"),
            "duration": int(duration_in_minutes),
            "password": validated_data.get("password"),
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "end_date_time": end_date_time.astimezone(pytz.UTC).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if end_date_time
            else None,
            "repeat_type": repeat_type,
            "repeat_interval": repeat_interval,
            "monthly_day": monthly_day,
            "weekly_days": weekly_days,
        }
        meeting_details = meeting_provider.create_meeting(meeting_config)
        meeting_instance = Meeting(
            variant=variant,
            start_time=start_time,
            duration=duration,
            end_date_time=end_date_time,
            repeat_type=repeat_type,
            repeat_interval=repeat_interval,
            monthly_day=monthly_day,
            weekly_days=weekly_days,
            course_session=validated_data.get("course_session"),
            subject=validated_data.get("subject"),
            meeting_id=meeting_details.get("id"),
            host_id=meeting_details.get("host_id"),
            host_email=meeting_details.get("host_email"),
            topic=meeting_details.get("topic"),
            meeting_type=meeting_details.get("type"),
            occurence_status=meeting_details.get("status"),
            password=meeting_details.get("password"),
            created_at=meeting_details.get("created_at"),
            agenda=meeting_details.get("agenda"),
        )
        meeting_instance.save()
        return meeting_instance


class SubjectCRUDSerializer(serializers.ModelSerializer):
    """Serializer for CRUD of subject."""

    class Meta:
        model = Subject
        fields = ("id", "name")
