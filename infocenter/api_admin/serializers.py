from rest_framework import serializers

from common.api.serializers import CreatorSerializer

from ..models import CourseInfo, CourseInfoCategory, WebResouce


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


class WebResouceCRUDAdminSerializer(CreatorSerializer):
    """WebResouce serializer."""

    class Meta:
        model = WebResouce
        fields = CreatorSerializer.Meta.fields + (
            "id",
            "title",
            "description",
            "file_resource",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields
