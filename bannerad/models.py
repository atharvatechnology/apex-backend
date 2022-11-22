from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CreatorBaseModel

# Create your models here.


class BannerAd(CreatorBaseModel):
    """Model for bannerad."""

    title = models.CharField(_("title"), max_length=100)
    description = models.CharField(_("description"), max_length=300)
    is_displayed = models.BooleanField(_("is_displayed"), default=False)

    class Meta:
        """Meta definition for BannerAd."""

        verbose_name = "BannerAd"
        verbose_name_plural = "BannerAds"
        ordering = ["-id"]

    def __str__(self):
        """Unicode representation of BannerAd."""
        return self.title
