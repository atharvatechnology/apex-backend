from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CreatorBaseModel

User = get_user_model()

# Create your models here.


class EnrollmentStatus:
    ACTIVE = "active"  # student can access all the enrolled objects
    INACTIVE = "inactive"  # enrollment/access has expired
    PENDING = "pending"  # enrollment is awaiting admin verification/payment
    CANCELLED = "cancelled"  # enrollment is abruply expired
    CHOICES = [
        (ACTIVE, "active"),
        (INACTIVE, "inactive"),
        (PENDING, "pending"),
        (CANCELLED, "cancelled"),
    ]


class Enrollment(models.Model):
    """Model definition for Enrollment."""

    student = models.ForeignKey(
        User,
        verbose_name=_("student"),
        related_name="enrolls",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        _("status"),
        max_length=32,
        choices=EnrollmentStatus.CHOICES,
        default=EnrollmentStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: add course field here after course app is created
    # courses = models.ManyToManyField(Course, verbose_name=_(
    #     "courses"), related_name="enrolls", blank=True)
    exams = models.ManyToManyField(
        "exams.Exam",
        verbose_name=_("exams"),
        related_name="enrolls",
        blank=True,
        through="ExamThroughEnrollment",
    )

    class Meta:
        """Meta definition for Enrollment."""

        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

    def __str__(self):
        """Unicode representation of Enrollment."""
        # TODO: make this more readable for admin panel
        return f"{self.student.__str__()} at {self.created_at}"


class SessionStatus:
    ACTIVE = "active"  # session is active
    INACTIVE = "inactive"  # session is inactive
    ENDED = "ended"  # session has ended
    CHOICES = [
        (ACTIVE, "active"),
        (INACTIVE, "inactive"),
        (ENDED, "ended"),
    ]


class Session(CreatorBaseModel):
    """Model definition for Session."""

    start_date = models.DateTimeField(_("start_date"))
    end_date = models.DateTimeField(_("end_date"))
    status = models.CharField(
        _("status"),
        max_length=32,
        choices=SessionStatus.CHOICES,
        default=SessionStatus.INACTIVE,
    )
    exam = models.ForeignKey(
        "exams.Exam",
        verbose_name=_("exam"),
        related_name="sessions",
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta definition for Session."""

        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self):
        """Unicode representation of Session."""
        return f"id{self.id}_createdAt{self.created_at}"


class ExamEnrollmentStatus:
    CREATED = (
        "created"  # student has enrolled in the exam but not yet attempted the exam
    )
    ATTEMPTED = "attempted"  # student has attempted the exam
    STARTED = "started"
    FINISHED = "finished"
    FAILED = "failed"  # student has failed the attempt
    PASSED = "passed"  # student has passed the latest attempt
    COMPLETED = "completed"  # exam has been completed
    CHOICES = [
        (CREATED, "created"),
        (ATTEMPTED, "attempted"),
        (STARTED, "started"),
        (FINISHED, "finished"),
        (FAILED, "failed"),
        (PASSED, "passed"),
        (COMPLETED, "completed"),
    ]


class ExamThroughEnrollment(models.Model):
    """Model definition for ExamThroughEnrollment."""

    enrollment = models.ForeignKey(
        Enrollment,
        verbose_name=_("enrollment"),
        related_name="exam_enrolls",
        on_delete=models.CASCADE,
    )
    exam = models.ForeignKey(
        "exams.Exam",
        verbose_name=_("exam"),
        related_name="exam_enrolls",
        on_delete=models.CASCADE,
    )
    selected_session = models.ForeignKey(
        Session,
        verbose_name=_("exam_session"),
        related_name="session_enrolls",
        on_delete=models.CASCADE,
    )
    score = models.DecimalField(
        _("score"), max_digits=5, decimal_places=2, default=Decimal("0.0")
    )
    status = models.CharField(
        _("status"),
        max_length=32,
        choices=ExamEnrollmentStatus.CHOICES,
        default=ExamEnrollmentStatus.CREATED,
    )
    # submitted = models.BooleanField(_("submitted"), default=False)

    class Meta:
        """Meta definition for ExamThroughEnrollment."""

        verbose_name = "ExamThroughEnrollment"
        verbose_name_plural = "ExamThroughEnrollments"

    def __str__(self):
        """Unicode representation of ExamThroughEnrollment."""
        return f"enrollment {self.enrollment} for exam {self.exam}"

    def __change_status(self, status):
        self.status = status
        self.save()

    @property
    def current_status(self):
        return self.status

    # FSM State transition methods
    def attempt_exam(self):
        self.__change_status(ExamEnrollmentStatus.ATTEMPTED)

    def fail_exam(self):
        self.__change_status(ExamEnrollmentStatus.FAILED)

    def pass_exam(self):
        self.__change_status(ExamEnrollmentStatus.PASSED)

    def complete_exam(self):
        self.__change_status(ExamEnrollmentStatus.COMPLETED)

    def calculate_score(self):
        """Return score of exam_enroll.

        Parameters
        ----------
        self : ExamThroughEnrollment
            exam_enroll whose score is to be calculated

        Returns
        -------
        int
            score of exam_enroll

        """
        pos_score = 0
        neg_score = 0
        for question_state in self.question_states.all():
            question = question_state.question
            option = question_state.selected_option
            if not option:
                continue
            if option.correct:
                pos_score += question.section.pos_marks
            else:
                neg_score += question.section.neg_marks
        return pos_score - neg_score


# TODO: add course enrollment model here after course app is created


class QuestionEnrollment(models.Model):
    """Model definition for QuestionEnrollment."""

    # examinee = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
    #     "examinee"), on_delete=models.CASCADE, related_name='question_states')
    exam_stat = models.ForeignKey(
        ExamThroughEnrollment,
        verbose_name=_("exam_stat"),
        on_delete=models.CASCADE,
        related_name="question_states",
    )
    question = models.ForeignKey(
        "exams.Question",
        verbose_name=_("question"),
        related_name=_("user_states"),
        on_delete=models.CASCADE,
    )
    selected_option = models.ForeignKey(
        "exams.Option",
        verbose_name=_("selected_option"),
        related_name=_("user_choices"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(_("upadated_at"), auto_now=True)

    def save(self, *args, **kwargs):
        try:
            self.exam_stat.exam.questions.get(pk=self.question.id)
            if self.selected_option:
                self.question.options.get(pk=self.selected_option.id)
            super().save(*args, **kwargs)
        except Exception as error:
            raise error

    class Meta:
        """Meta definition for QuestionEnrollment."""

        verbose_name = "QuestionEnrollment"
        verbose_name_plural = "QuestionEnrollments"
        ordering = ["-updated_at"]

    def __str__(self):
        """Unicode representation of QuestionEnrollment."""
        return f"option {self.exam_stat} by {self.question} for {self.selected_option}"
