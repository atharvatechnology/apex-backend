from django.contrib import admin

from bannerad.models import BannerAd


@admin.register(BannerAd)
class BannerAdAdmin(admin.ModelAdmin):
    """Admin for BannerAd."""

    list_displaye = (
        "id",
        "title",
        "description",
        "is_displayed",
    )
