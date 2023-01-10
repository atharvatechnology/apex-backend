import django_filters

from attendance.models import Attendance, StudentAttendance, TeacherAttendance


class AttendanceFilter(django_filters.FilterSet):
    """Filter for attendance."""

    class Meta:
        model = Attendance
        fields = {"date": ["exact", "gte", "lte"]}


class StudentAttendanceDateFilter(django_filters.FilterSet):
    """Filter for Student Attendance by date."""

    class Meta:
        model = StudentAttendance
        fields = {"date": ["exact", "gte", "lte"]}


class TeacherAttendanceDateFilter(django_filters.FilterSet):
    """Filter for Teacher Attendance by date."""

    class Meta:
        model = TeacherAttendance
        fields = {"date": ["exact", "gte", "lte"]}
