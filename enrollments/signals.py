from asgiref.sync import async_to_sync
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ExamEnrollmentStatus, SessionStatus
from .tasks import calculate_score

channel_layer = get_channel_layer()
logger = get_task_logger("__name__")
CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


@receiver(post_save, sender="enrollments.ExamThroughEnrollment")
def on_exam_attempt(sender, instance, **kwargs):
    if instance.status == ExamEnrollmentStatus.ATTEMPTED:
        calculate_score.delay(instance.id)


@receiver(post_save, sender="enrollments.Session")
def on_exam_session_save(sender, instance, **kwargs):
    if instance.status == SessionStatus.INACTIVE:
        print("session inactive")
        instance.exam.schedule_exam()

    elif instance.status == SessionStatus.ACTIVE:
        print("session active")
        instance.exam.start_exam()
        async_to_sync(channel_layer.group_send)(
            # "clock",
            f"exam_{instance.exam.id}",
            {"type": "get_exam", "status": instance.exam.status},
        )

    elif instance.status == SessionStatus.ENDED:
        print("session ended")
        instance.exam.finish_exam()
        # prevent further enrollment into that session
        # prevent further submissions into that ExamEnrollment
        # start the calculation of the score
        # cache the total number of exam enrollments in that session
        total_examinees = instance.session_enrolls.count()
        cache.set(
            f"session_{instance.id}_total_examinees", total_examinees, timeout=CACHE_TTL
        )
        cache.set(f"session_{instance.id}_total_results", 0, timeout=CACHE_TTL)

        for exam_through_enrollment in instance.session_enrolls.all():
            if exam_through_enrollment.status == ExamEnrollmentStatus.CREATED:
                exam_through_enrollment.attempt_exam()
            # scoring calculation automatically beigns after
            # exam is attempted
            # session_id = exam_through_enrollment.selected_session.id
            session_id = instance.id
            result_count = cache.get(f"session_{session_id}_total_results")
            result_count += 1
            cache.set(
                f"session_{session_id}_total_results",
                result_count,
            )

            total_examinees = cache.get(f"session_{session_id}_total_examinees")
            # check if all exam enrollments are calculated
            if result_count >= total_examinees:
                # publish session exam results
                # session = Session.objects.get(id=session_id)
                instance.publish_results()

    elif instance.status == SessionStatus.RESULTSOUT:
        print("session results out")
        # clear the cache
        cache.delete(f"session_{instance.id}_total_results")
        cache.delete(f"session_{instance.id}_total_examinees")
        # broadcast that the results are out
        async_to_sync(channel_layer.group_send)(
            f"exam_{instance.exam.id}",
            {
                "type": "get_session_status",
                "is_published": instance.is_visible
                and (instance.status == SessionStatus.RESULTSOUT),
            },
        )
