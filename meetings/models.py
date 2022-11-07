from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .providers.register import provider_factory


class Subject(models.Model):
    """Model definition for Subject."""

    name = models.CharField(max_length=200)

    class Meta:
        """Meta definition for Subject."""

        ordering = ("name",)
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name


class MeetingProviderVariants:
    keys = provider_factory.get_providers()
    CHOICES = [(key, key) for key in keys]


class Meeting(models.Model):
    """Model definition for Meeting."""

    meeting_id = models.CharField(max_length=200)
    variant = models.CharField(
        _("variant"),
        choices=MeetingProviderVariants.CHOICES,
        max_length=32,
        default="zoom",
    )
    host_id = models.CharField(_("host_id"), max_length=255)
    host_email = models.EmailField(_("host_email"))
    topic = models.CharField(_("topic"), max_length=255)
    meeting_type = models.IntegerField(_("meeting_type"))
    occurence_status = models.CharField(_("occurence_status"), max_length=64)
    start_time = models.DateTimeField(_("start_time"))
    password = models.CharField(_("password"), max_length=10)
    created_at = models.DateTimeField(_("createdAt"))
    agenda = models.CharField(_("agenda"), max_length=255)
    duration = models.DurationField(_("duration"))
    course_session = models.ForeignKey(
        "enrollments.CourseSession",
        verbose_name=_("course_session"),
        related_name="meetings",
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name=_("subject"),
        related_name="classes",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    end_date_time = models.DateTimeField(_("end_date_time"), null=True, blank=True)
    monthly_day = models.PositiveIntegerField(
        _("monthly_day"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
    )
    repeat_interval = models.PositiveIntegerField(_("repeat_interval"), default=1)
    repeat_type = models.PositiveIntegerField(
        _("repeat_type"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
    )
    weekly_days = models.CharField(
        _("weekly_days"), max_length=255, null=True, blank=True
    )

    def __str__(self):
        return f"{self.topic}_{self.id} - {self.start_time}"

    class Meta:
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"
