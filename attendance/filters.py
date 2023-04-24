import django_filters

from attendance.models import Attendance


class AttendanceFilter(django_filters.FilterSet):
    """Filter for attendance."""

    date = django_filters.DateFilter(field_name="date__date")

    class Meta:
        model = Attendance
        fields = {"date": ["exact", "gte", "lte", "year", "month"]}
