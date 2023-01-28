from common.api.serializers import CreatorSerializer
from physicalbook.models import PhysicalBook

# class PhysicalBookCreateSerializer(CreatorSerializer):
#     """Seralizer class for create view."""

#     class Meta:
#         model = PhysicalBook
#         fields = CreatorSerializer.Meta.fields + (
#             "name",
#             "image",
#             "course",
#         )
#         read_only_fields = CreatorSerializer.Meta.read_only_fields


class PhysicalBookSerializerAfterEnroll(CreatorSerializer):
    """serializer class for PhysicalBookRetrieveAPIViewAfterEnroll."""

    class Meta:
        model = PhysicalBook
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "image",
            "course",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class PhysicalBookSerializerBeforeEnroll(CreatorSerializer):
    """serializer class for PhysicalBookRetrieveAPIViewAfterEnroll."""

    class Meta:
        model = PhysicalBook
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "image",
            "course",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields
