from rest_framework import serializers

from common.api.serializers import CreatorSerializer

from ..models import CourseInfo, CourseInfoCategory, WebResouce


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


class WebResouceListSerializer(CreatorSerializer):
    """List WebResouce serializer."""

    class Meta:
        model = WebResouce
        fields = CreatorSerializer.Meta.fields + (
            "id",
            "title",
            "description",
            "file_resource",
        )
