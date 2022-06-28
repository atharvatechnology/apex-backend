import json
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from common.errors import StateTransitionError
from common.modelFields import ZeroSecondDateTimeField
from common.models import CreatorBaseModel, PublishedModel, PublishedQueryset
from common.validators import validate_date_time_gt_now

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
    courses = models.ManyToManyField(
        "courses.Course", through="CourseThroughEnrollment", related_name="enrolls"
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
    RESULTSOUT = "resultsout"  # session has ended and results are out
    CHOICES = [
        (ACTIVE, "active"),
        (INACTIVE, "inactive"),
        (ENDED, "ended"),
        (RESULTSOUT, "resultsout"),
    ]


class SessionQuerySet(PublishedQueryset, models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            tasks = PeriodicTask.objects.filter(name__in=[obj.start_task, obj.end_task])
            tasks.delete()
            obj.delete()
        super().delete(*args, **kwargs)


class Session(PublishedModel, CreatorBaseModel):
    """Model definition for Session."""

    objects = SessionQuerySet.as_manager()
    start_date = ZeroSecondDateTimeField(
        _("start_date"), validators=[validate_date_time_gt_now]
    )
    end_date = ZeroSecondDateTimeField(
        _("end_date"), validators=[validate_date_time_gt_now]
    )
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

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError(
                _("Start_date should be less than End_date"), code="invalid_date"
            )
        if self.start_date == self.end_date:
            raise ValidationError(
                _("Start_date should not be same as End_date"), code="invalid_date"
            )

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
        self.exam.finish_exam()
        self.delete_tasks()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Set up tasks on create session."""
        if not self.id:
            super().save(*args, **kwargs)
            self.setup_tasks()
        # else:
        #     # filter the tasks by session id
        #     tasks = PeriodicTask.objects.filter(
        #         name__in=[self.start_task, self.end_task]
        #     )

        #     # tasks = PeriodicTask.objects.filter(kwargs=json.dumps(
        #     # {"session_id": f"{self.id}"}))
        #     # delete the tasks
        #     tasks.delete()
        # self.setup_tasks()
        super().save(*args, **kwargs)

    def setup_tasks(self):
        """Create the tasks for the session."""

        start_date_aware = self.start_date
        end_date_aware = self.end_date
        if timezone.is_naive(self.start_date):
            start_date_aware = timezone.make_aware(
                self.start_date, timezone=settings.CELERY_TIMEZONE
            )
        else:
            start_date_aware = timezone.localtime(self.start_date)

        if timezone.is_naive(self.end_date):
            end_date_aware = timezone.make_aware(
                self.end_date, timezone=settings.CELERY_TIMEZONE
            )
        else:
            end_date_aware = timezone.localtime(self.end_date)

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
            name=f"{self.exam.name}_{start_date_aware}_{self.id} start task",
            task="enrollments.tasks.start_exam_session",
            kwargs=json.dumps({"session_id": f"{self.id}"}),
            one_off=True,
        )
        end_task = PeriodicTask.objects.create(
            crontab=end_schedule,
            name=f"{self.exam.name}_{end_date_aware}_{self.id} end task",
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
        human_readable_date = self.created_at.strftime("%Y-%m-%d %H:%M %p")
        return f"id - {self.id} - createdAt - {human_readable_date}"

    def __change_status(self, status):
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

    def publish_results(self):
        if self.status == SessionStatus.RESULTSOUT:
            return
        if self.status == SessionStatus.ENDED:
            return self.__change_status(SessionStatus.RESULTSOUT)
        raise StateTransitionError(f"Session cannot be activated from {self.status}")


class CourseEnrollmentStatus:
    NEW = "new"  # 1st phase or recently enrolled
    INITIATED = "initiated"  # Started the course
    ONHOLD = "on-hold"  # If paused for certain time
    PROGRESS = "progress"  # Go with the flow or Continue the course
    DECLINED = "declined"  # Unsubscribed/Stop/leave that course in between
    FINALPHASE = "final phase"  # Stage after 75% completion
    COMPLETED = "completed"  # 100% course completion

    CHOICES = [
        (NEW, "new"),
        (INITIATED, "initiated"),
        (ONHOLD, "on-hold"),
        (PROGRESS, "progress"),
        (DECLINED, "declined"),
        (FINALPHASE, "final phase"),
        (COMPLETED, "completed"),
    ]


class CourseThroughEnrollment(models.Model):
    """Model defination for CourseEnrollment."""

    course = models.ForeignKey(
        "courses.Course", related_name="course_enrolls", on_delete=models.CASCADE
    )
    enrollment = models.ForeignKey(
        Enrollment, related_name="course_enrolls", on_delete=models.CASCADE
    )
    selected_session = models.ForeignKey(
        Session, related_name="course_enrolls", on_delete=models.CASCADE
    )
    course_status = models.CharField(
        max_length=50,
        choices=CourseEnrollmentStatus.CHOICES,
        default=CourseEnrollmentStatus.NEW,
    )
    completed_date = models.DateTimeField()

    class Meta:
        """Meta defination for CourseThroughEnrollment."""

        verbose_name = "CourseThroughEnrollment"
        verbose_name_plural = "CourseThroughEnrollments"

    def __str__(self):
        """Unicode representation of CourseEnrollment."""
        return f"course {self.course} for {self.enrollment}enrollment"

    def __change_course_status(self, course_status):
        self.course_status = course_status

    @property
    def current_course_status(self):
        return self.course_status

    def initiated_course(self):
        if self.course_status == CourseEnrollmentStatus.INITIATED:
            return
        elif self.course_status == CourseEnrollmentStatus.NEW:
            return self.__change_course_status(CourseEnrollmentStatus.INITIATED)
        raise StateTransitionError(
            f"Cannot be enrolled to new course at {self.course_status} status"
        )

    def progress_course(self):
        if self.course_status == CourseEnrollmentStatus.PROGRESS:
            return
        elif self.course_status in [
            CourseEnrollmentStatus.INITIATED,
            CourseEnrollmentStatus.FINALPHASE,
            CourseEnrollmentStatus.ONHOLD,
        ]:
            return self.__change_course_status(CourseEnrollmentStatus.PROGRESS)
        raise StateTransitionError(
            f"Cannot be able to initiated course at {self.course_status} status"
        )

    def decline_course(self):
        if self.course_status == CourseEnrollmentStatus.DECLINED:
            return
        elif self.course_status in [
            CourseEnrollmentStatus.INITIATED,
            CourseEnrollmentStatus.PROGRESS,
            CourseEnrollmentStatus.FINALPHASE,
            CourseEnrollmentStatus.ONHOLD,
        ]:
            return self.__change_course_status(CourseEnrollmentStatus.DECLINED)
        raise StateTransitionError(
            f"Cannot be able to Declined course. Current status is {self.course_status}"
        )

    def on_hold_course(self):
        if self.course_status == CourseEnrollmentStatus.ONHOLD:
            return
        elif self.course_status in [
            CourseEnrollmentStatus.INITIATED,
            CourseEnrollmentStatus.PROGRESS,
            CourseEnrollmentStatus.FINALPHASE,
        ]:
            return self.__change_course_status(CourseEnrollmentStatus.ONHOLD)
        raise StateTransitionError(
            f"Cannot be able to be at on hold state during {self.course_status} state"
        )

    def finalphase_course(self):
        if self.course_status == CourseEnrollmentStatus.FINALPHASE:
            return
        elif self.course_status == CourseEnrollmentStatus.PROGRESS:
            return self.__change_course_status(CourseEnrollmentStatus.FINALPHASE)
        raise StateTransitionError(
            f"Cannot be able be at Final stage of course in {self.course_status} status"
        )

    def complete_course(self):
        if self.course_status == CourseEnrollmentStatus.COMPLETED:
            return
        if self.course_status in [
            CourseEnrollmentStatus.FINALPHASE,
            CourseEnrollmentStatus.PROGRESS,
        ]:
            return self.__change_course_status(CourseEnrollmentStatus.COMPLETED)
        raise StateTransitionError(
            f"Cannot be able to complete course. Current status is {self.course_status}"
        )


class PhysicalBookCourseEnrollment(models.Model):
    """Model defination of EnrollmentToPhysicalBookCourse."""

    physical_book = models.ForeignKey(
        "physicalbook.PhysicalBook",
        on_delete=models.CASCADE,
        related_name="physicalbook_enrolls",
    )
    course_enrollment = models.ForeignKey(
        CourseThroughEnrollment,
        on_delete=models.CASCADE,
        related_name="physicalbook_enrolls",
    )
    status_provided = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.physical_book} book for {self.course_enrollment} course enrollment"
        )


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
                neg_marks = question.section.neg_percentage * question.section.pos_marks
                neg_score += neg_marks
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
