from common.api.serializers import CreatorSerializer
from notes.models import Content, Note


class ContentSerializer(CreatorSerializer):
    class Meta:
        model = Content
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "description",
            "type",
            "file",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class NoteSerializer(CreatorSerializer):
    content = ContentSerializer(many=True)

    class Meta:
        model = Note
        fields = CreatorSerializer.Meta.fields + ("title", "content")
        read_only_fields = CreatorSerializer.Meta.read_only_fields
