from rest_framework import permissions

from enrollments.models import EnrollmentStatus


def is_exam_enrolled_active(enrolled_obj, request, view):
    """Return True if user has active enrollment for that obj.

    Parameters
    ----------
    enrolled_obj : exam/course
        obj to which user is enrolled into
    request : request
        request object
    view : view
        view object

    Returns
    -------
    bool
        state of active enrollment of user to that obj

    """
    if request.user.is_authenticated:
        student_enrollment = view._get_student_enrollment(enrolled_obj)
        request.student_enrollment = student_enrollment
        if student_enrollment:
            if student_enrollment.status == EnrollmentStatus.ACTIVE:
                return True
    return False


class IsExamEnrolledActive(permissions.BasePermission):
    """Permission to allow only the enrolled users to use the obj."""

    code = "EXAM ALREADY SUBMITTED"
    message = "You have already attempted the exam."

    def has_object_permission(self, request, view, obj):
        return is_exam_enrolled_active(obj, request, view)
