from rest_framework import serializers

from physicalbook.api_admin.serializers import PhysicalBookAdminListSerializer

from ..models import Course


class CourseMinSerializer(serializers.ModelSerializer):
    """Course Mini Serializer."""

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class CoursePhysicalSerializer(serializers.ModelSerializer):
    """Course Mini Serializer."""

    physical_books = PhysicalBookAdminListSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "physical_books",
        )
        read_only_fields = fields
