from django.db import models


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
