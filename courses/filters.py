import django_filters

from courses.models import Course


class CourseFilter(django_filters.FilterSet):
    """Filter for courses."""

    class Meta:
        model = Course
        fields = {
            "price": ["gt", "lt"],
            "category": ["exact"],
            "name": ["icontains"],
            "created_at": ["gt", "lt"],
            "status": ["exact"],
        }


class CourseDropdownFilter(django_filters.FilterSet):
    """Filter for courses dropdown."""

    class Meta:
        model = Course
        fields = {
            "category": ["exact"],
            "status": ["exact"],
        }
