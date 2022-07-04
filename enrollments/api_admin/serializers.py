from django.utils import timezone
from rest_framework import serializers

from common.api.serializers import CreatorSerializer, PublishedSerializer
from enrollments.models import Session


class SessionAdminSerializer(CreatorSerializer, PublishedSerializer):
    """Serializer for Session create."""

    class Meta:
        model = Session
        fields = (
            CreatorSerializer.Meta.fields
            + PublishedSerializer.Meta.fields
            + (
                "start_date",
                "end_date",
                "status",
                "exam",
            )
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)

    def validate_publish_date(self, value):
        """Validate publish date.

        value cannnot be before current datetime.
        value cannnot be before end_date.
        """

        if value < timezone.now():
            raise serializers.ValidationError("Publish date cannot be in the past.")
        if "end_date" in self.initial_data and value < self.initial_data["end_date"]:
            raise serializers.ValidationError("Publish date cannot be before end date.")
        return value


class SessionAdminUpdateSerializer(SessionAdminSerializer):
    """Serializer for Session update."""

    class Meta:
        model = Session
        fields = SessionAdminSerializer.Meta.fields
        read_only_fields = SessionAdminSerializer.Meta.read_only_fields + (
            "start_date",
            "end_date",
            "exam",
        )

    def validate_publish_date(self, value):
        """Validate publish date.

        imported other validation from validate_publish_date in SessionAdminSerializer.
        value cannnot be before end_date.
        """
        value = super().validate_publish_date(value)
        if hasattr(self.instance, "end_date") and value < self.instance.end_date:
            raise serializers.ValidationError("Publish date cannot be before end date.")
        return value
