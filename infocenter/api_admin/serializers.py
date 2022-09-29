from rest_framework import serializers

from ..models import CourseInfo, CourseInfoCategory


class CourseInfoListSerializer(serializers.ModelSerializer):
    """CourseInfo serializer."""

    class Meta:
        model = CourseInfo
        fields = ["id", "title", "description", "category"]


class CourseInfoCategoryListSerializer(serializers.ModelSerializer):
    """CourseInfoCategory serializer."""

    class Meta:
        model = CourseInfoCategory
        fields = ["id", "name"]


class CourseInfoCategoryCRUDSerializer(CourseInfoListSerializer):
    """CourseInfoCategory serializer."""

    courseinfos = CourseInfoListSerializer(many=True, read_only=True)

    class Meta:
        model = CourseInfoCategory
        fields = CourseInfoCategoryListSerializer.Meta.fields + ["courseinfos"]


class CourseInfoCRUDSerializer(serializers.ModelSerializer):
    """CourseInfo serializer."""

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
