from rest_framework import serializers

from bannerad.models import BannerAd


class BannerAdCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "img",
            "is_displayed",
        )


class BannerAdListSerializer(serializers.ModelSerializer):
    """Serializer for listing bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "img",
            "is_displayed",
        )


class BannerAdUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "img",
            "is_displayed",
        )


class BannerAdRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "img",
            "is_displayed",
        )