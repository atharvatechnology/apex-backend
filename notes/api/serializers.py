from common.api.serializers import CreatorSerializer
from notes.models import Content, Note


class ContentSerializerAfterEnroll(CreatorSerializer):
    class Meta:
        model = Content
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "description",
            "type",
            "file",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class ContentSerializerBeforeEnroll(CreatorSerializer):
    class Meta:
        model = Content
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "description",
            "type",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class NoteSerializerBeforeEnroll(CreatorSerializer):
    content = ContentSerializerBeforeEnroll(many=True)

    class Meta:
        model = Note
        fields = CreatorSerializer.Meta.fields + ("title", "content")
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class NoteSerializerAfterEnroll(CreatorSerializer):
    content = ContentSerializerAfterEnroll(many=True)

    class Meta:
        model = Note
        fields = CreatorSerializer.Meta.fields + ("title", "content")
        read_only_fields = CreatorSerializer.Meta.read_only_fields
