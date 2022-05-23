from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CreatorBaseModel
from common.validators import validate_positive


class ExamTemplate(CreatorBaseModel):
    """Model definition for ExamTemplate."""

    name = models.CharField(max_length=100)
    # description = models.TextField(blank=True)
    duration = models.IntegerField(default=0, validators=[validate_positive])
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pass_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    display_num_questions = models.IntegerField(
        default=0, validators=[validate_positive]
    )
    # exam_type = models.CharField(max_length=10, choices=(
    #     ('S', 'SINGLE'), ('M', 'MULTIPLE')), default='S')

    class Meta:
        verbose_name = _("Exam Template")
        verbose_name_plural = _("Exam Templates")

    def __str__(self):
        return self.name


# Create your models here.
class Exam(CreatorBaseModel):
    """Model definition for Exam."""

    name = models.CharField(_("name"), max_length=128)
    category = models.ManyToManyField(
        "courses.CourseCategory",
        verbose_name=_("categories"),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    # TODO: Add course field here after course app is created
    # Also how to relate course to exams?
    # course = models.ForeignKey("courses.Course",
    #                            verbose_name=_("course"),
    #                            related_name="%(app_label)s_%(class)s_related",
    #                            related_query_name="%(app_label)s_%(class)ss",
    #                            on_delete=models.SET_NULL,
    #                            null=True,
    #                            blank=True)
    price = models.DecimalField(
        _("price"),
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.0"),
        validators=[validate_positive],
    )
    template = models.ForeignKey(
        ExamTemplate,
        verbose_name=_("template"),
        related_name="exams",
        on_delete=models.CASCADE,
    )
    # tags = models.ManyToManyField("tags.Tag", verbose_name=_("tags"), blank=True)
    # full marks and pass marks are attribute of the exam template

    class Meta:
        """Meta definition for Exam."""

        verbose_name = "Exam"
        verbose_name_plural = "Exams"
        ordering = ["-created_at"]

    def __str__(self):
        """Unicode representation of Exam."""
        return self.name
