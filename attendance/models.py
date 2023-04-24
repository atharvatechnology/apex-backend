from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CreatorBaseModel

User = get_user_model()


class Attendance(CreatorBaseModel):
    """Attendance model."""

    date = models.DateTimeField(_("Attended date"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user} - {self.date.strftime('%Y-%m-%d %H:%M %p')}"


class StudentAttendance(Attendance):
    """Student attendance model."""

    pass


class TeacherAttendanceDetailCategory:
    """Teacher attendance detail category model."""

    DRAFT = "draft"
    REQUEST = "request"
    APPROVE = "approve"
    REJECT = "reject"
    CLARIFICATION = "clarification"
    CHOICES = (
        (DRAFT, _("Draft")),
        (REQUEST, _("Request")),
        (APPROVE, _("Approve")),
        (REJECT, _("Reject")),
        (CLARIFICATION, _("Clarification")),
    )


class TeacherAttendance(Attendance):
    """Teacher attendance model."""

    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name or ""


class TeacherAttendanceDetail(CreatorBaseModel):
    """Teacher attendance detail model."""

    number_of_period = models.DecimalField(
        _("Number_of_peroid"), decimal_places=2, max_digits=4
    )
    message = models.TextField(_("Message"))
    remarks = models.TextField(_("Remarks"), blank=True, null=True)
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=TeacherAttendanceDetailCategory.CHOICES,
        default=TeacherAttendanceDetailCategory.DRAFT,
    )
    teacher_attendance = models.ForeignKey(
        TeacherAttendance, on_delete=models.CASCADE, related_name="details"
    )

    section = models.TextField(_("section"))
    subject = models.TextField(_("subject"))
    class_note = models.TextField(_("class_note"))
    start_time = models.TimeField(_("start_time"), null=True, blank=True)
    end_time = models.TimeField(_("end_time"), null=True, blank=True)

    def __str__(self):
        return f"{self.teacher_attendance.user.username} - {self.status}"

    class Meta:
        ordering = ["-created_at"]
