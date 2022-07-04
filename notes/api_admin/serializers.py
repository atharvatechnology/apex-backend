import os

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
        field to ContentSerializer

    """

    file_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Content
        fields = (
            "name",
            "description",
            "type",
            "file",
            "note",
            "content",
            "file_name",
        ) + CreatorSerializer.Meta.fields
        read_only_fields = CreatorSerializer.Meta.read_only_fields
        extra_kwargs = {
            "type": {"required": True},
        }

    def get_file_name(self, obj):
        return os.path.basename(obj.file.name) if obj.file else None

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("Content is required")
        return value

    def validate_file(self, value):
        request = self.context["request"]
        if (
            "file" in request.FILES
            and not request.FILES["file"]
            or "file" not in request.FILES
        ):
            raise serializers.ValidationError("File is required")
        return value

    def validate_type(self, value):
        if value == ContentType.PDF:
            if (
                self.instance is None
                and not self.initial_data["file"]
                or self.instance is not None
                and not self.instance.file
            ):
                raise serializers.ValidationError("File property is required")
        elif value == ContentType.TEXT:
            if not self.initial_data["content"]:
                raise serializers.ValidationError("Content property is required")
        return value


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
