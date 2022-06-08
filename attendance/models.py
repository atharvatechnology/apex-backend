from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CreatorBaseModel

User = get_user_model()


class Attendance(CreatorBaseModel):
    """Attendance model."""

    date = models.DateTimeField(_("Attendance date"))
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

    pass


class TeacherAttendanceDetail(CreatorBaseModel):
    """Teacher attendance detail model."""

    number_of_peroid = models.IntegerField(_("Number of peroid"))
    message = models.TextField(_("Message"))
    remarks = models.TextField(_("Remarks"))
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=TeacherAttendanceDetailCategory.CHOICES,
        default=TeacherAttendanceDetailCategory.DRAFT,
    )
    teacher_attendance = models.OneToOneField(
        TeacherAttendance, on_delete=models.CASCADE, related_name="details"
    )

    def __str__(self):
        return f"{self.teacher_attendance.user.username} - {self.status}"

    class Meta:
        ordering = ["-created_at"]
