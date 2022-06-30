from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CourseCategory(models.Model):
    """Model for course category."""

    name = models.CharField(
        _("name"),
        max_length=100,
    )
    description = models.CharField(
        _("description"),
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for CourseCategory."""

        verbose_name = "CourseCategory"

        verbose_name = "CourseCategory"
        verbose_name_plural = "CourseCategories"
        ordering = ["id"]

    def __str__(self):
        """Unicode representation of CourseCategory."""
        return self.name


class CourseStatus:
    INSESSION = "insession"  # course has active classses currently.
    UPCOMING = "upcoming"  # course is being planned.
    ENDED = "ended"  # course has successfully ended.
    CANCELLED = "cancelled"  # course has been abruptly ended.

    CHOICES = [
        (INSESSION, "insession"),
        (UPCOMING, "upcoming"),
        (ENDED, "ended"),
        (CANCELLED, "cancelled"),
    ]


class Course(models.Model):
    """Model definition for Course."""

    name = models.CharField(
        _("name"),
        max_length=100,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        CourseCategory,
        verbose_name=_("category"),
        related_name="courses",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    description = models.CharField(
        _("password"),
        max_length=100,
        blank=True,
        null=True,
    )

    link = models.URLField(
        _("link"),
        max_length=150,
        blank=True,
        null=True,
    )
    password = models.CharField(
        _("password"),
        max_length=128,
        help_text=_(
            "Use'[algo]$[salt]$[hexdigest]' or use the \
                < a href=\"password/\">change password form</a>."
        ),
        blank=True,
        null=True,
    )
    status = models.CharField(
        _("status"),
        max_length=64,
        choices=CourseStatus.CHOICES,
        default=CourseStatus.UPCOMING,
    )
    price = models.DecimalField(
        _("price"),
        max_digits=7,
        decimal_places=2,
        default=Decimal("0.0"),
    )

    class Meta:
        """Meta definition for Course."""

        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["-id"]

    def __str__(self):
        """Unicode representation of Course."""
        return self.name
