from common.api.serializers import CreatorSerializer
from notes.models import Content, Note, RecordedVideo


class ContentCreateSerializer(CreatorSerializer):
    """serializer class for create view.

    Parameters
    ----------
    CreatorSerializer : cls

        serializer provides additional fields
        (created_at, updated_at, created_by, updated_by)
        to content create serializer

    """

    class Meta:
        model = Content
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "description",
            "type",
            "file",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class ContentSerializerAfterEnroll(CreatorSerializer):
    """serializer for ContentRetrieveAPIViewAfterEnroll to enrolled user.

    Parameters
    ----------
    CreatorSerializer : cls

        inheritated serializer
        class which provides additional
        field to
        ContentSerializerAfterEnroll

    """

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
    """serializer for ContentRetrieveAPIViewBeforeEnroll view for unenrolled user.

    Parameters
    ----------
    CreatorSerializer : cls

        inheritated serializer
        class which provides additional
        field to ContentSerializerAfterEnroll

    """

    class Meta:
        model = Content
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "description",
            "type",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class NoteCreateSerializer(CreatorSerializer):
    """serializer for NoteCreateAPIView view.

    Parameters
    ----------
    CreatorSerializer : cls
        inheritated serializer
        class which provides additional
        field to NoteCreateSerializer

    """

    contents = ContentSerializerBeforeEnroll(many=True)

    class Meta:
        model = Note
        fields = CreatorSerializer.Meta.fields + ("title", "contents")
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class NoteSerializerBeforeEnroll(CreatorSerializer):
    """serializer for NoteRetrieveAPIViewBeforeEnroll view for unenrolled user.

    Parameters
    ----------
    CreatorSerializer : cls
        inheritated serializer
        class which provides additional
        field to NoteCreateSerializer

    """

    class Meta:
        model = Note
        fields = CreatorSerializer.Meta.fields + ("title",)
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class NoteSerializerAfterEnroll(CreatorSerializer):
    """serializer for NoteRetrieveAPIViewAfterEnroll view for enrolled user.

    Parameters
    ----------
    CreatorSerializer : cls
        inheritated serializer
        class which provides additional
        field to NoteCreateSerializer

    """

    contents = ContentSerializerAfterEnroll(many=True)

    class Meta:
        model = Note
        fields = CreatorSerializer.Meta.fields + ("title", "contents")
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class RecordedVideoListSerializer(CreatorSerializer):
    class Meta:
        model = RecordedVideo
        fields = CreatorSerializer.Meta.fields + ("date", "link", "course")
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class RecordedVideoDetailSerializer(CreatorSerializer):
    class Meta:
        model = RecordedVideo
        fields = CreatorSerializer.Meta.fields + ("date", "link", "course")
        read_only_fields = CreatorSerializer.Meta.read_only_fields
