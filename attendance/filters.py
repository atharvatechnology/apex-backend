import django_filters

from attendance.models import Attendance


class AttendanceFilter(django_filters.FilterSet):
    """Filter for attendance."""

    date_only = django_filters.DateFilter(field_name="date", lookup_expr="date")
    date__gte = django_filters.DateFilter(field_name="date", lookup_expr="date__gte")
    date__lte = django_filters.DateFilter(field_name="date", lookup_expr="date__lte")

    class Meta:
        model = Attendance
        fields = ["date"]
        # fields = {"date": ["exact", "gte", "lte"]}
