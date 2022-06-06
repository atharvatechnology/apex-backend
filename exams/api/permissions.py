from rest_framework import permissions

from enrollments.models import ExamEnrollmentStatus


def is_exam_enrolled_active(enrolled_obj, user):
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
    if user.is_authenticated:
        student_enrollments = enrolled_obj.enrolls.all().filter(student=user)
    if student_enrollments.count() > 0:
        student_enrollment = student_enrollments.first()
        exam_enrollment = (
            student_enrollment.exam_enrolls.all().filter(exam=enrolled_obj).first()
        )
        if exam_enrollment.status == ExamEnrollmentStatus.CREATED:
            return True
    return False


class IsExamEnrolledActive(permissions.BasePermission):
    """Permission to allow only the enrolled users to use the obj."""

    code = "EXAM ALREADY SUBMITTED"
    message = "You have already attempted the exam."

    def has_object_permission(self, request, view, obj):
        return is_exam_enrolled_active(obj, request.user)
