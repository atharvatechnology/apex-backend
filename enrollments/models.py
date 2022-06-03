import json
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from common.errors import StateTransitionError
from common.models import CreatorBaseModel

User = get_user_model()

# Create your models here.


class EnrollmentStatus:
    ACTIVE = "active"  # student can access all the enrolled objects
    # usually after payment is done
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


class SessionQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            tasks = PeriodicTask.objects.filter(name__in=[obj.start_task, obj.end_task])
            tasks.delete()
            obj.delete()
        super().delete(*args, **kwargs)


class Session(CreatorBaseModel):
    """Model definition for Session."""

    objects = SessionQuerySet.as_manager()
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
    start_task = models.CharField(
        _("start_task"), max_length=256, null=True, blank=True
    )
    end_task = models.CharField(_("end_task"), max_length=256, null=True, blank=True)

    def delete_tasks(self):
        tasks = PeriodicTask.objects.filter(name__in=[self.start_task, self.end_task])
        # delete the tasks
        tasks.delete()

    # TODO: Add delete which deletes the tasks on session delete
    def delete(self, *args, **kwargs):
        """Delete the tasks on session delete."""
        # filter the tasks by the session id
        # tasks = PeriodicTask.objects.filter(kwargs={"session_id": self.id})
        # alternatively you can do this
        # # filter the tasks by task names

        self.delete_tasks()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Set up tasks on create session."""
        if not self.id:
            super().save(*args, **kwargs)
        else:
            # filter the tasks by session id
            tasks = PeriodicTask.objects.filter(
                name__in=[self.start_task, self.end_task]
            )

            # tasks = PeriodicTask.objects.filter(kwargs=json.dumps(
            # {"session_id": f"{self.id}"}))
            # delete the tasks
            tasks.delete()
        self.setup_tasks()
        super().save(*args, **kwargs)

    def setup_tasks(self):
        """Create the tasks for the session."""
        from django.conf import settings
        from django.utils.timezone import is_naive, localtime, make_aware

        start_date_aware = self.start_date
        end_date_aware = self.end_date
        if is_naive(self.start_date):
            start_date_aware = make_aware(
                self.start_date, timezone=settings.CELERY_TIMEZONE
            )
        else:
            start_date_aware = localtime(self.start_date)
        if is_naive(self.end_date):
            end_date_aware = make_aware(
                self.end_date, timezone=settings.CELERY_TIMEZONE
            )
        else:
            end_date_aware = localtime(self.end_date)

        start_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=start_date_aware.minute,
            hour=start_date_aware.hour,
            day_of_week="*",
            day_of_month=start_date_aware.day,
            month_of_year=start_date_aware.month,
        )
        end_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=end_date_aware.minute,
            hour=end_date_aware.hour,
            day_of_week="*",
            day_of_month=end_date_aware.day,
            month_of_year=end_date_aware.month,
        )
        start_task = PeriodicTask.objects.create(
            crontab=start_schedule,
            name=f"{self.exam.name}_{start_date_aware} start task",
            task="enrollments.tasks.start_exam_session",
            kwargs=json.dumps({"session_id": f"{self.id}"}),
            one_off=True,
        )
        end_task = PeriodicTask.objects.create(
            crontab=end_schedule,
            name=f"{self.exam.name}_{end_date_aware} end task",
            task="enrollments.tasks.end_exam_session",
            kwargs=json.dumps({"session_id": f"{self.id}"}),
            one_off=True,
        )
        self.start_task = start_task.name
        self.end_task = end_task.name
        # self.save()

    class Meta:
        """Meta definition for Session."""

        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self):
        """Unicode representation of Session."""
        return f"id{self.id}_createdAt{self.created_at}"

    def __change_status(self, status):
        print(f"state has been changed from {self.status} {status}")
        self.status = status
        self.save()

    def activate_session(self):
        if self.status == SessionStatus.ACTIVE:
            return
        if self.status == SessionStatus.INACTIVE:
            return self.__change_status(SessionStatus.ACTIVE)
        raise StateTransitionError(f"Session cannot be activated from {self.status}")

    def end_session(self):
        if self.start_task:
            self.delete_tasks()
        if self.status == SessionStatus.ENDED:
            return
        if self.status == SessionStatus.ACTIVE:
            return self.__change_status(SessionStatus.ENDED)
        raise StateTransitionError(f"Session cannot be ended from {self.status}")


class ExamEnrollmentStatus:
    CREATED = (
        "created"  # student has enrolled in the exam but not yet attempted the exam
    )
    ATTEMPTED = "attempted"  # student has attempted the exam
    # STARTED = "started"
    # FINISHED = "finished"
    FAILED = "failed"  # student has failed the attempt
    PASSED = "passed"  # student has passed the latest attempt
    COMPLETED = "completed"  # exam has been completed
    CHOICES = [
        (CREATED, "created"),
        (ATTEMPTED, "attempted"),
        # (STARTED, "started"),
        # (FINISHED, "finished"),
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
    # TODO: Look into django FSM
    def attempt_exam(self):
        if self.status == ExamEnrollmentStatus.ATTEMPTED:
            return
        if self.status == ExamEnrollmentStatus.CREATED:
            return self.__change_status(ExamEnrollmentStatus.ATTEMPTED)
        raise StateTransitionError(
            f"Cannot attempt exam. Current status is {self.status}"
        )

    def fail_exam(self):
        if self.status == ExamEnrollmentStatus.FAILED:
            return
        if self.status == ExamEnrollmentStatus.ATTEMPTED:
            return self.__change_status(ExamEnrollmentStatus.FAILED)
        raise StateTransitionError(f"Cannot fail exam. Current status is {self.status}")

    def pass_exam(self):
        if self.status == ExamEnrollmentStatus.PASSED:
            return
        if self.status == ExamEnrollmentStatus.ATTEMPTED:
            return self.__change_status(ExamEnrollmentStatus.PASSED)
        raise StateTransitionError(f"Cannot pass exam. Current status is {self.status}")

    # def complete_exam(self):
    #     if self.status == ExamEnrollmentStatus.ATTEMPTED:
    #         self.__change_status(ExamEnrollmentStatus.COMPLETED)
    #     self.__change_status(ExamEnrollmentStatus.COMPLETED)

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
            # if not option:
            #     continue
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
    )
    updated_at = models.DateTimeField(_("upadated_at"), auto_now=True)

    def save(self, *args, **kwargs):
        try:
            self.exam_stat.exam.questions.get(pk=self.question.id)
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
