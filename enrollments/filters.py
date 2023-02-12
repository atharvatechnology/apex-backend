import django_filters

from courses.models import CourseCategory
from enrollments.models import CourseThroughEnrollment, ExamThroughEnrollment


class ExamThroughEnrollmentFilter(django_filters.FilterSet):
    """Filter for ExamThroughEnrollment."""

    created_at = django_filters.DateFromToRangeFilter(
        field_name="enrollment__created_at"
    )

    class Meta:
        model = ExamThroughEnrollment
        fields = {
            "exam": ["exact"],
            "exam__id": ["exact"],
            "selected_session__start_date": ["exact"],
            "selected_session": ["exact"],
            "enrollment__status": ["exact"],
        }


class CourseThroughEnrollmentFilter(django_filters.FilterSet):
    """Filter for ExamThroughEnrollment."""

    created_at = django_filters.DateFromToRangeFilter(
        field_name="enrollment__created_at"
    )

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
        }


class CourseGraphFilter(django_filters.FilterSet):
    """Filter for Course Graph."""

    class Meta:
        model = CourseCategory
        fields = {"name": ["icontains"]}
