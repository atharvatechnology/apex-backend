import django_filters

from courses.models import Course
from exams.models import Exam


class ExamFilter(django_filters.FilterSet):
    """filter for exam course."""

    class Meta:
        model = Exam
        fields = {"course_id": ["exact"]}


class ExamOnCourseFilter(django_filters.FilterSet):
    """filter for exam course."""

    course_future = django_filters.NumberFilter(method="filter_course_future")

    class Meta:
        model = Exam
        fields = {
            "course_id": ["exact"],
            "exam_type": ["exact"],
            "created_at": ["gt", "lt"],
        }

    def filter_course_future(self, queryset, name, value):
        """Filter for future exams."""
        course = Course.objects.get(id=value)
        return queryset.filter(created_at__gt=course.created_at, course__isnull=True)
