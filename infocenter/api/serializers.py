from rest_framework import serializers

from ..models import CourseInfo, CourseInfoCategory


class CourseInfoCategoryRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve CourseInfoCategory serializer."""

    class Meta:
        model = CourseInfoCategory
        fields = ["id", "name"]


class CourseInfoRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve CourseInfo serializer."""

    category = CourseInfoCategoryRetrieveSerializer()

    class Meta:
        model = CourseInfo
        fields = [
            "id",
            "title",
            "description",
            "category",
            "introduction",
            "eligibility",
            "syllabus",
            "colleges",
        ]
