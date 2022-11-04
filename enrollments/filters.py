import django_filters

from enrollments.models import CourseThroughEnrollment, ExamThroughEnrollment


class ExamThroughEnrollmentFilter(django_filters.FilterSet):
    """Filter for ExamThroughEnrollment."""

    class Meta:
        model = ExamThroughEnrollment
        fields = {"exam", "selected_session"}


class CourseThroughEnrollmentFilter(django_filters.FilterSet):
    """Filter for CourseThroughEnrollment."""

    class Meta:
        model = CourseThroughEnrollment
        fields = {"course", "selected_session"}
