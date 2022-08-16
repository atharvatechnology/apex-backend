from rest_framework import serializers

from courses.models import Course, CourseCategory


class CourseCategorySerializer(serializers.ModelSerializer):
    """Serializer for creating course categories."""

    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
        )


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for creating courses."""

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "status",
            "price",
            "category",
            "description",
            "password",
            "link",
            "image",
            "duration",
        )
