import django_filters

from courses.models import Course


class CourseFilter(django_filters.FilterSet):
    """Filter for courses."""

    class Meta:
        model = Course
        fields = {"price": ["gt", "lt"], "category": ["exact"]}
