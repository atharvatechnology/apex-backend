from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from attendance.api_admin.serializers import (
    StudentAttendanceAdminListSerializer,
    TeacherAttendanceAdminListSerializer,
)
from attendance.filters import AttendanceFilter
from attendance.models import StudentAttendance, TeacherAttendance
from common.paginations import StandardResultsSetPagination


class StudentAttendanceAdminListAPIView(ListAPIView):
    """View for listing admin student attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentAttendanceAdminListSerializer
    queryset = StudentAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = AttendanceFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get the queryset."""
        student_id = self.kwargs.get("student_id", None)
        if not student_id:
            raise ValidationError("Student id is required.")

        return super().get_queryset().filter(user=self.kwargs.get("student_id"))


class TeacherAttendanceAdminListAPIView(ListAPIView):
    """View for listing admin teacher attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = TeacherAttendanceAdminListSerializer
    queryset = TeacherAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = AttendanceFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get the queryset."""
        teacher_id = self.kwargs.get("teacher_id", None)
        if not teacher_id:
            raise ValidationError("Teacher id is required.")

        return super().get_queryset().filter(user=self.kwargs.get("teacher_id"))
