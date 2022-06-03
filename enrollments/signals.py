from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ExamEnrollmentStatus, SessionStatus
from .tasks import calculate_score


@receiver(post_save, sender="enrollments.ExamThroughEnrollment")
def on_exam_attempt(sender, instance, **kwargs):
    if instance.status == ExamEnrollmentStatus.ATTEMPTED:
        calculate_score.delay(instance.id)


@receiver(post_save, sender="enrollments.Session")
def on_exam_session_save(sender, instance, **kwargs):
    if instance.status == SessionStatus.INACTIVE:
        print("session inactive")
        instance.exam.schedule_exam()
    if instance.status == SessionStatus.ACTIVE:
        print("session active")
        instance.exam.start_exam()
    if instance.status == SessionStatus.ENDED:
        print("session ended")
        instance.exam.finish_exam()
        # prevent further enrollment into that session
        # prevent further submissions into that ExamEnrollment
        # start the calculation of the score
        for exam_through_enrollment in instance.session_enrolls.all():
            exam_through_enrollment.attempt_exam()
            # scoring calculation automatically beigns after
            # exam is attempted
