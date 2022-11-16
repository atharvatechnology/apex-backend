from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.validators import PhoneNumberValidator

User = get_user_model()


# Create your models here.
class Counseling(models.Model):
    """Model for counseling."""

    phone_validator = PhoneNumberValidator()
    student_name = models.CharField(_("student_name"), max_length=100)
    counsellor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="counsellor", blank=True, null=True
    )
    note = models.CharField(_("note"), max_length=150)
    phone_number = models.CharField(
        _("phone_number"), max_length=50, validators=[phone_validator]
    )
    date = models.DateField(_("date"))

    class Meta:
        """Meta definition for Counseling."""

        verbose_name = "Counseling"
        verbose_name_plural = "Counselings"
        ordering = ["-id"]

    def __str__(self):
        """Unicode representation of Counseling."""
        return self.student_name
