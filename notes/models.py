from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CreatorBaseModel
from courses.models import Course


class ContentType:
    PDF = "pdf"
    TEXT = "text"

    CHOICES = [
        (PDF, "PDF"),
        (TEXT, "Text"),
    ]


class Note(CreatorBaseModel):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(
        Course, related_name="notes", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["id"]


class BaseContent(CreatorBaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Content(BaseContent):
    def content_location(self, filename):
        return f"content/note-{self.note.id}/{filename}"

    type = models.CharField(
        _("Type"), max_length=10, choices=ContentType.CHOICES, default=ContentType.PDF
    )
    file = models.FileField(upload_to=content_location, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name="contents", blank=True, null=True
    )

    class Meta:
        ordering = ["id"]


class RecordedVideo(BaseContent):

    date = models.DateTimeField(_("Entry Date"))
    link = models.URLField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="recorded_videos",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["id"]
