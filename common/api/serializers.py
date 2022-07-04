from rest_framework import serializers

from common.models import CreatorBaseModel, PublishedModel


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorBaseModel
        fields = (
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )


class PublishedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishedModel
        fields = (
            "is_published",
            "publish_date",
        )
