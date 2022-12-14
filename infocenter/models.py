from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CreatorBaseModel


class CourseInfoCategory(models.Model):
    """Model definition for CourseInfoCategory."""

    name = models.CharField(max_length=128)

    class Meta:
        """Meta definition for CourseInfoCategory."""

        verbose_name = "CourseInfoCategory"
        verbose_name_plural = "CourseInfoCategorys"

    def __str__(self):
        """Unicode representation of CourseInfoCategory."""
        return f"{self.name}"


class CourseInfo(models.Model):
    """Model definition for CourseInfo."""

    # TODO: Define fields here
    title = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(
        CourseInfoCategory, on_delete=models.CASCADE, related_name="courseinfos"
    )
    introduction = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    syllabus = models.TextField(blank=True)
    colleges = models.TextField(blank=True)

    class Meta:
        """Meta definition for CourseInfo."""

        verbose_name = "CourseInfo"
        verbose_name_plural = "CourseInfos"

    def __str__(self):
        """Unicode representation of CourseInfo."""
        return f"{self.id}_{self.title}"


class WebResource(CreatorBaseModel):
    """Model definition for WebResource."""

    def resource_upload(self, filename):
        """To upload resource."""
        splitted_filename = filename.split(".")
        # rename the file attaching the creation timestamp
        filename_with_timestamp = (
            f"{splitted_filename[0]}_"
            + f"{self.created_at.strftime('%Y/%m/%d-%H-%M-%S')}.{splitted_filename[1]}"
        )
        return f"web_resources/{filename_with_timestamp}"

    title = models.CharField(_("title"), max_length=128)
    description = models.TextField(_("description"), blank=True)
    file_resource = models.FileField(_("file_resource"), upload_to=resource_upload)
