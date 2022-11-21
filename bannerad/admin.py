from django.contrib import admin

from bannerad.models import BannerAd

# Register your models here.


@admin.register(BannerAd)
class BannerAdAdmin(admin.ModelAdmin):
    """Admin for BannerAd Model."""

    list_display = (
        "id",
        "title",
        "description",
        "is_displayed",
    )
