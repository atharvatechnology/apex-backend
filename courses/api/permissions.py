from rest_framework import permissions

from enrollments.models import EnrollmentStatus


def is_course_enrolled_active(enrolled_obj, user):
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
        # course_enrollment = (
        #     student_enrollment.course_enrolls.all().filter(course=enrolled_obj).first()
        # )
        # if course_enrollment.course_enroll_status == CourseEnrollmentStatus.NEW:
        #     return True
        if student_enrollment.status == EnrollmentStatus.ACTIVE:
            return True
    return False


class IsCourseEnrolledActive(permissions.BasePermission):
    """Permission to allow only the enrolled users to use the obj."""

    code = "COURSE ALREADY SUBMITTED"
    message = "Please enroll to view course."

    def has_object_permission(self, request, view, obj):
        return is_course_enrolled_active(obj, request.user)
