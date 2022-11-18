from rest_framework import serializers

from bannerads.models import BannerAd


class BannerAdCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "title",
            "description",
            "is_displayed",
        )
