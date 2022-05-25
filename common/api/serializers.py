from rest_framework import serializers

from common.models import CreatorBaseModel


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
