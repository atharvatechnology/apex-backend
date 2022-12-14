from rest_framework import serializers

from common.api.serializers import CreatorSerializer
from physicalbook.models import PhysicalBook


class PhysicalBookAdminListSerializer(serializers.ModelSerializer):
    """Serializer for listing physicalbook for admin."""

    class Meta:
        model = PhysicalBook
        fields = (
            "name",
            "image",
            "course",
        )


class PhysicalBookAdminRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving physicalbook for admin."""

    class Meta:
        model = PhysicalBook
        fields = (
            "name",
            "image",
            "course",
        )


class PhysicalBookAdminCreateSerializer(CreatorSerializer):
    """Serializer for creating physicalbook for admin."""

    class Meta:
        model = PhysicalBook
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "image",
            "course",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class PhysicalBookAdminUpdateSerializer(CreatorSerializer):
    """Serializer for updating physicalbook for admin."""

    class Meta:
        model = PhysicalBook
        fields = (
            "name",
            "image",
            "course",
        )
