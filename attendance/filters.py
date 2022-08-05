import django_filters

from attendance.models import Attendance


class AttendanceFilter(django_filters.FilterSet):
    """Filter for attendance."""

    class Meta:
        model = Attendance
        fields = {"date": ["exact", "gt", "lt"], "user": ["exact"]}
