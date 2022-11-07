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


class DynamicFieldsCategorySerializer:
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ModelFieldsSerializer(serializers.Serializer):
    """Serializer for getting model fields."""

    model_fields = serializers.ListField(child=serializers.CharField(max_length=55))

    class Meta:
        fields = "model_fields"
