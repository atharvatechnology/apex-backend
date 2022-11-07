import django_filters

from enrollments.models import CourseThroughEnrollment, ExamThroughEnrollment


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
        }


class CourseThroughEnrollmentFilter(django_filters.FilterSet):
    """Filter for ExamThroughEnrollment."""

    class Meta:
        model = CourseThroughEnrollment
        fields = {
            "course__id": ["exact"],
            "course__name": ["icontains"],
            "selected_session__start_date": ["exact"],
            "selected_session": ["exact"],
            "enrollment__status": ["exact"],
        }
