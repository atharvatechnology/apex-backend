from rest_framework import serializers

from bannerad.models import BannerAd


class BannerAdRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "title",
            "description",
            "is_displayed",
        )
