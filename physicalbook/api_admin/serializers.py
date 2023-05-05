from rest_framework import serializers

from common.api.serializers import CreatorSerializer
from physicalbook.models import PhysicalBook


class PhysicalBookAdminListSerializer(serializers.ModelSerializer):
    """Serializer for listing physicalbook for admin."""

    class Meta:
        model = PhysicalBook
        fields = (
            "id",
            "name",
            "image",
            "course",
            "sub_topic",
        )


class PhysicalBookAdminRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving physicalbook for admin."""

    class Meta:
        model = PhysicalBook
        fields = (
            "id",
            "name",
            "image",
            "course",
            "sub_topic",
        )


class PhysicalBookAdminCreateSerializer(CreatorSerializer):
    """Serializer for creating physicalbook for admin."""

    class Meta:
        model = PhysicalBook
        fields = CreatorSerializer.Meta.fields + (
            "id",
            "name",
            "image",
            "course",
            "sub_topic",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class PhysicalBookAdminUpdateSerializer(CreatorSerializer):
    """Serializer for updating physicalbook for admin."""

    class Meta:
        model = PhysicalBook
        fields = (
            "id",
            "name",
            "image",
            "course",
            "sub_topic",
        )


class PhysicalBookEnrolledCourseSerializer(serializers.ModelSerializer):

    taken = serializers.SerializerMethodField()

    class Meta:
        model = PhysicalBook
        fields = (
            "id",
            "name",
            "taken",
            "sub_topic",
        )

    def get_taken(self, obj):
        student_id = self.context["view"].kwargs.get("student_id")
        return bool(
            obj.physicalbook_enrolls.filter(
                course_enrollment__enrollment__student__id=student_id,
                status_provided=True,
            )
        )
