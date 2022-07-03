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


class SessionAdminUpdateSerializer(CreatorSerializer, PublishedSerializer):
    """Serializer for Session update."""

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
        read_only_fields = CreatorSerializer.Meta.read_only_fields + (
            "status",
            "start_date",
            "end_date",
            "exam",
        )
