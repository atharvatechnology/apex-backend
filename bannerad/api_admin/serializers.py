from rest_framework import serializers

from bannerad.models import BannerAd


class BannerAdCreateAdminSerializer(serializers.ModelSerializer):
    """Serializer for creating bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "img",
            "is_displayed",
        )


class BannerAdListAdminSerializer(serializers.ModelSerializer):
    """Serializer for listing bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "img",
            "is_displayed",
        )


class BannerAdUpdateAdminSerializer(serializers.ModelSerializer):
    """Serializer for creating bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "img",
            "is_displayed",
        )


class BannerAdRetrieveAdminSerializer(serializers.ModelSerializer):
    """Serializer for retrieving bannerad."""

    class Meta:
        model = BannerAd
        fields = (
            "id",
            "img",
            "is_displayed",
        )
