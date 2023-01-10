import django_filters

from attendance.models import Attendance, StudentAttendance, TeacherAttendance


class AttendanceFilter(django_filters.FilterSet):
    """Filter for attendance."""

    date_only = django_filters.DateFilter(field_name="date", lookup_expr="date")
    date__gte = django_filters.DateFilter(field_name="date", lookup_expr="date__gte")
    date__lte = django_filters.DateFilter(field_name="date", lookup_expr="date__lte")

    class Meta:
        model = Attendance
        fields = ["date"]
        # fields = {"date": ["exact", "gte", "lte"]}


class StudentAttendanceDateFilter(django_filters.FilterSet):
    """Filter for Student Attendance by date."""

    date_only = django_filters.DateFilter(field_name="date", lookup_expr="date")
    date__gte = django_filters.DateFilter(field_name="date", lookup_expr="date__gte")
    date__lte = django_filters.DateFilter(field_name="date", lookup_expr="date__lte")

    class Meta:
        model = StudentAttendance
        fields = ["date"]


class TeacherAttendanceDateFilter(django_filters.FilterSet):
    """Filter for Teacher Attendance by date."""

    date_only = django_filters.DateFilter(field_name="date", lookup_expr="date")
    date__gte = django_filters.DateFilter(field_name="date", lookup_expr="date__gte")
    date__lte = django_filters.DateFilter(field_name="date", lookup_expr="date__lte")

    class Meta:
        model = TeacherAttendance
        fields = ["date"]
