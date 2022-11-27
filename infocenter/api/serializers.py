from rest_framework import serializers

from common.api.serializers import CreatorSerializer

from ..models import CourseInfo, CourseInfoCategory, WebResource


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


class WebResourceListSerializer(CreatorSerializer):
    """List WebResource serializer."""

    class Meta:
        model = WebResource
        fields = CreatorSerializer.Meta.fields + (
            "id",
            "title",
            "description",
            "file_resource",
        )
