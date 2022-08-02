from rest_framework import serializers

from enrollments.models import EnrollmentStatus, ExamThroughEnrollment


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
    all_examinee_states = ExamThroughEnrollment.objects.filter(exam=obj.exam)
    num_examinee = all_examinee_states.count()
    num_examinee_lower_score = all_examinee_states.filter(score__lt=obj.score).count()
    return num_examinee - num_examinee_lower_score


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
