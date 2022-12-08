import django_filters

from attendance.models import Attendance


class AttendanceFilter(django_filters.FilterSet):
    """Filter for attendance."""

    date_only = django_filters.DateFilter(field_name="date", lookup_expr="date")
    date__gt = django_filters.DateFilter(field_name="date", lookup_expr="date__gt")
    date__lt = django_filters.DateFilter(field_name="date", lookup_expr="date__lt")

    class Meta:
        model = Attendance
        fields = ["date"]
        # fields = {"date": ["exact", "gt", "lt"]}
