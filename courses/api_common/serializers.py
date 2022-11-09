from rest_framework import serializers

from ..models import Course


class CourseMinSerializer(serializers.ModelSerializer):
    """Course Mini Serializer."""

    class Meta:
        model = Course
        fields = ("id", "name")
        read_only_fields = fields
