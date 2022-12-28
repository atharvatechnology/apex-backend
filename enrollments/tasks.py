from celery import shared_task
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from enrollments.models import CourseSession, ExamSession, ExamThroughEnrollment
from exams.models import ExamType

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


@shared_task
def calculate_score(exam_through_enrollment_id):
    """Calculate score for a given exam through enrollment.

    Score the exam submission and update the score in the database.
    Pass/Fail the submission based on the score.

    Parameters
    ----------
    exam_through_enrollment_id : int
        id of exam through enrollment

    """
    exam_through_enrollment = ExamThroughEnrollment.objects.get(
        id=exam_through_enrollment_id
    )
    (
        exam_through_enrollment.score,
        exam_through_enrollment.negative_score,
    ) = exam_through_enrollment.calculate_score()
    # exam_through_enrollment.save()
    pass_marks = (
        exam_through_enrollment.exam.template.pass_percentage
        * exam_through_enrollment.exam.template.full_marks
    )
    if exam_through_enrollment.score >= pass_marks:
        # pass trigger
        exam_through_enrollment.pass_exam()
    else:
        # fail trigger
        exam_through_enrollment.fail_exam()
    if exam_through_enrollment.exam.exam_type == ExamType.PRACTICE:
        exam_through_enrollment.selected_session.end_session()
    # session_id = exam_through_enrollment.selected_session.id
    # result_count = cache.get_or_set(
    #         f"session_{session_id}_total_results",
    #         0,
    #         timeout=CACHE_TTL
    #     )
    # result_count += 1
    # cache.set(
    #     f"session_{session_id}_total_results",
    #     result_count,
    # )

    # total_examinees = cache.get(
    #     f"session_{session_id}_total_examinees")
    # # check if all exam enrollments are calculated
    # if total_examinees and (result_count >= total_examinees):
    #     # publish session exam results
    #     session = Session.objects.get(id=session_id)
    #     session.publish_results()


# from django_celery_beat.models import PeriodicTask

# create a schedule like this
#  schedule, _ = CrontabSchedule.objects.get_or_create(
#     ...: minute=alarm_time.minute,
#     ...: hour=alarm_time.hour,
#     ...: day_of_week='*',
#     ...: day_of_month=alarm_time.day,
#     ...: month_of_year=alarm_time.month
#     ...: )

# Create a one-off task like so

# PeriodicTask.objects.create(
#     ...: crontab=schedule,
#     ...: name="hello periodic task new",
#  ...: task="nameoftask",
#     ...: one_off=True
#     ...: )


@shared_task
def start_exam_session(session_id):
    """Start session.

    Start the exam for a given session.

    Parameters
    ----------
    session_id : int
        id of session

    """
    # activate session
    session = ExamSession.objects.get(id=session_id)
    session.activate_session()


@shared_task
def end_exam_session(session_id):
    """Finish session.

    Finish the exam for a given session.

    Parameters
    ----------
    session_id : int
        id of session

    """
    # deactivate session
    session = ExamSession.objects.get(id=session_id)
    session.end_session()


@shared_task
def start_course_session(session_id):
    session = CourseSession.objects.get(id=session_id)
    session.activate_session()


@shared_task
def end_course_session(session_id):
    session = CourseSession.objects.get(id=session_id)
    session.end_session()
