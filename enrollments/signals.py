from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ExamEnrollmentStatus
from .tasks import calculate_score


@receiver(post_save, sender="enrollments.ExamThroughEnrollment")
def on_exam_attempt(sender, instance, **kwargs):
    if instance.status == ExamEnrollmentStatus.ATTEMPTED:
        calculate_score.delay(instance.id)
