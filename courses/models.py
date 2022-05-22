from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CourseStatus:
    INSESSION = "insession"
    UPCOMING = "upcoming"
    ENDED = "ended"
    CANCELLED = "cancelled"

    CHOICES = [
        (INSESSION, "insession"),
        (UPCOMING, "upcoming"),
        (ENDED, "ended"),
        (CANCELLED, "cancelled"),
    ]


class Course(models.Model):
    name = models.CharField(_("name"), max_length=100)
    type_id = models.IntegerField(_("type_id"))
    instructor_id = models.IntegerField(_("instructor_id"))
    link = models.URLField(_("link"), max_length=150, blank=True, null=True)
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

    class Meta:
        "Meta definition for Course."
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["created_at"]

    def __str__(self):
        "Unicode representation of Course."
        return self.name
