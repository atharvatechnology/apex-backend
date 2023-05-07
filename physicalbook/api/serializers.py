from rest_framework import serializers

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

    taken = serializers.SerializerMethodField()

    class Meta:
        model = PhysicalBook
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "image",
            "course",
            "sub_topic",
            "taken",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    def get_taken(self, obj):
        student_id = self.context["request"].user.id
        return bool(
            obj.physicalbook_enrolls.filter(
                course_enrollment__enrollment__student__id=student_id,
                status_provided=True,
            )
        )


class PhysicalBookSerializerBeforeEnroll(CreatorSerializer):
    """serializer class for PhysicalBookRetrieveAPIViewAfterEnroll."""

    class Meta:
        model = PhysicalBook
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "image",
            "course",
            "sub_topic",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields
