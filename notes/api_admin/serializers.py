from rest_framework import serializers

from common.api.serializers import CreatorSerializer
from notes.models import Content, ContentType, Note, RecordedVideo


class NoteSerializer(CreatorSerializer):
    """serializer for NoteCreateAPIView view.

    Parameters
    ----------
    CreatorSerializer : cls
        inheritated serializer
        class which provides additional
        field to NoteCreateSerializer

    """

    class Meta:
        model = Note
        fields = ("title", "course") + CreatorSerializer.Meta.fields
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class ContentSerializer(CreatorSerializer):
    """serializer for ContentCreateAPIView view.

    Parameters
    ----------
    CreatorSerializer : cls
        inheritated serializer
        class which provides additional
        field to ContentCreateSerializer

    """

    class Meta:
        model = Content
        fields = (
            "name",
            "description",
            "type",
            "file",
            "note",
            "content",
        ) + CreatorSerializer.Meta.fields
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    def validate(self, attrs):
        if attrs["type"] == ContentType.PDF:
            if (
                hasattr(attrs, "file")
                and not self.initial_data["file"]
                or not hasattr(attrs, "file")
            ):
                raise serializers.ValidationError("file is required")
        elif attrs["type"] == ContentType.TEXT:
            if (
                hasattr(attrs, "content")
                and not self.initial_data["content"]
                or not hasattr(attrs, "content")
            ):
                raise serializers.ValidationError("content is required")
        return attrs


class RecordedVideoSerializer(CreatorSerializer):
    """serializer for RecordedVideoCreateAPIView view.

    Parameters
    ----------
    CreatorSerializer : cls
        inheritated serializer
        class which provides additional
        field to RecordedVideoCreateSerializer

    """

    class Meta:
        model = RecordedVideo
        fields = (
            "name",
            "description",
            "date",
            "link",
            "course",
        ) + CreatorSerializer.Meta.fields
        read_only_fields = CreatorSerializer.Meta.read_only_fields
