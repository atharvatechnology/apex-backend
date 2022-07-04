from rest_framework import serializers

from courses.models import Course, CourseCategory
from notes.api.serializers import NoteSerializerAfterEnroll, NoteSerializerBeforeEnroll
from physicalbook.api.serializers import (
    PhysicalBookSerializerAfterEnroll,
    PhysicalBookSerializerBeforeEnroll,
)


class CourseRetrieveSerializerBeforeEnroll(serializers.ModelSerializer):
    """Serializer for retrieving courses."""

    notes = NoteSerializerBeforeEnroll(many=True)
    physical_books = PhysicalBookSerializerBeforeEnroll(many=True)

    class Meta:

        model = Course
        fields = ("id", "name", "status", "price", "notes", "physical_books")


class CourseRetrieveSerializerAfterEnroll(serializers.ModelSerializer):
    """Serializer for retrieving courses."""

    notes = NoteSerializerAfterEnroll(many=True)
    physical_books = PhysicalBookSerializerAfterEnroll(many=True)

    class Meta:

        model = Course
        fields = (
            "id",
            "name",
            "link",
            "password",
            "status",
            "price",
            "notes",
            "physical_books",
        )


class CourseCategoryRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving course categories."""

    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
        )
