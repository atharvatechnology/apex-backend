import django_filters

from enrollments.models import ExamThroughEnrollment


class ExamThroughEnrollmentFilter(django_filters.FilterSet):
    """Filter for ExamThroughEnrollment."""

    class Meta:
        model = ExamThroughEnrollment
        fields = {
            "exam":["exact"], 
            "selected_session__start_date":["exact"]
            }
