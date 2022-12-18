import django_filters

from courses.models import Course
from enrollments.models import Enrollment


class CourseCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = {"category": ["exact"]}


class ExamDateFilter(django_filters.FilterSet):
    created_at = django_filters.DateRangeFilter()
    created_at__year = django_filters.NumberFilter(
        field_name="created_at", lookup_expr="year"
    )

    class Meta:
        model = Enrollment
        fields = ["created_at", "created_at__year"]
