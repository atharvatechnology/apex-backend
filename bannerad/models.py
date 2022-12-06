from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CreatorBaseModel


class BannerAd(CreatorBaseModel):
    """Model for BannerAd."""

    is_displayed = models.BooleanField(_("is_displayed"), default=False)
    img = models.ImageField(_("img"))

    class Meta:
        """Meta definition for BannerAd."""

        verbose_name = "BannerAd"
        verbose_name_plural = "BannerAds"
        ordering = ["-created_at"]
