import django_filters

from courses.models import CourseCategory
from enrollments.models import (
    CourseThroughEnrollment,
    ExamSession,
    ExamThroughEnrollment,
)


class ExamThroughEnrollmentFilter(django_filters.FilterSet):
    """Filter for ExamThroughEnrollment."""

    class Meta:
        model = ExamThroughEnrollment
        fields = {
            "exam": ["exact"],
            "exam__id": ["exact"],
            "selected_session__start_date": ["exact"],
            "selected_session": ["exact"],
            "enrollment__status": ["exact"],
            "created_at": ["gt", "lt"],
        }


class CourseThroughEnrollmentFilter(django_filters.FilterSet):
    """Filter for ExamThroughEnrollment."""

    class Meta:
        model = CourseThroughEnrollment
        fields = {
            "course__id": ["exact"],
            "course__name": ["icontains"],  # For Report
            "selected_session__start_date": ["exact"],
            "selected_session": ["exact"],
            "enrollment__status": ["exact"],
            "course_enroll_status": ["exact"],  # For Report
            "course__category__name": ["icontains"],  # For Report
            "created_at": ["gt", "lt"],
        }


class CourseGraphFilter(django_filters.FilterSet):
    """Filter for Course Graph."""

    class Meta:
        model = CourseCategory
        fields = {"name": ["icontains"]}


class ExamSessionFilter(django_filters.FilterSet):
    """Filter for ExamThroughEnrollment."""

    class Meta:
        model = ExamSession
        fields = {
            "start_date": ["exact"],
        }
