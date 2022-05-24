from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CreatorBaseModel


class ContentType:
    VIDEO = "video"
    AUDIO = "audio"
    PDF = "pdf"
    TEXT = "text"

    CHOICES = [
        (VIDEO, "Video"),
        (AUDIO, "Audio"),
        (PDF, "PDF"),
        (TEXT, "Text"),
    ]


class Note(CreatorBaseModel):
    title = models.CharField(max_length=200)
    # course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Content(models.Model):
    def content_location(instance, filename):
        return "content/{0}/{1}".format(instance.note.id, filename)

    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(
        _("Type"), max_length=10, choices=ContentType.CHOICES, default=ContentType.VIDEO
    )
    file = models.FileField(upload_to=content_location, blank=True, null=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
