from rest_framework import serializers

from enrollments.models import (
    EnrollmentStatus,
    ExamSession,
    ExamThroughEnrollment,
    SessionStatus,
)
from exams.models import ExamStatus


def is_enrolled(enrolled_obj, user):
    """Return True if user has enrollment for that obj.

    Parameters
    ----------
    enrolled_obj : exam/course
        obj to which user is enrolled into
    user : user
        whose enrollment is to be checked

    Returns
    -------
    bool
        state of enrollment of user to that obj

    """
    enrollments = []
    if user.is_authenticated:
        enrollments = enrolled_obj.enrolls.all().filter(student=user)
    if len(enrollments) > 0:
        return True
    return False


def is_enrolled_active(enrolled_obj, user):
    """Return True if user has active enrollment for that obj.

    Parameters
    ----------
    enrolled_obj : exam/course
        obj to which user is enrolled into
    user : user
        whose enrollment is to be checked

    Returns
    -------
    bool
        state of active enrollment of user to that obj

    """
    enrollments = []
    if user.is_authenticated:
        enrollments = enrolled_obj.enrolls.all().filter(
            student=user, status=EnrollmentStatus.ACTIVE
        )
    if len(enrollments) > 0:
        return True
    return False


def get_student_rank(obj):
    """Get the rank of the user in the exam.

    This is based on the score of current exam takers.

    Parameters
    ----------
    obj : ExamThroughEnrollment
        exam enrollment.

    Returns
    -------
    int
        rank of the user in the exam.

    """
    if obj.selected_session.status == "resultsout":
        all_examinee_states = ExamThroughEnrollment.objects.filter(
            exam=obj.exam, selected_session=obj.selected_session
        )
        num_examinee = all_examinee_states.count()
        num_examinee_lower_score = all_examinee_states.filter(
            score__lt=obj.score
        ).count()
        return num_examinee - num_examinee_lower_score
    else:
        return None


def batch_is_enrolled_and_price(enrolled_objs, user):
    sum_price = 0.0
    for enrolled_obj in enrolled_objs:
        sum_price += float(enrolled_obj.price)
        if is_enrolled(enrolled_obj, user):
            raise serializers.ValidationError(
                f"{user} is already enrolled into {enrolled_obj}"
            )
    return sum_price


def exam_data_save(exams_data, enrollment):
    if exams_data:
        for data in exams_data:
            exam = data.get("exam")
            selected_session = data.get("selected_session")
            ExamThroughEnrollment(
                enrollment=enrollment, exam=exam, selected_session=selected_session
            ).save()


# TODO Need to be discussed. Status send in List.
def retrieve_exam_status(self, obj):
    user = self.context["request"].user
    if not user.is_authenticated:
        return None
    enrollment = ExamThroughEnrollment.objects.filter(
        enrollment__student=user,
        exam=obj,
    ).first()
    if enrollment:
        session_id = enrollment.selected_session.id
        exam_session = ExamSession.objects.filter(id=session_id).first()
        if exam_session:
            if exam_session.status == SessionStatus.INACTIVE:
                return ExamStatus.SCHEDULED
            elif exam_session.status == SessionStatus.ACTIVE:
                return ExamStatus.IN_PROGRESS
        return ExamStatus.CREATED
    return ExamStatus.CREATED
