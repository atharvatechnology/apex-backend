from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from attendance.api_admin.serializers import (
    StudentAttendanceAdminListSerializer,
    StudentAttendanceAdminRetrieveSerializer,
    TeacherAttendanceAdminListSerializer,
    TeacherAttendanceAdminRetrieveSerializer,
)
from attendance.filters import AttendanceFilter
from attendance.models import StudentAttendance, TeacherAttendance


class StudentAttendanceAdminListAPIView(ListAPIView):
    """View for listing admin student attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentAttendanceAdminListSerializer
    queryset = StudentAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = AttendanceFilter

    def get_queryset(self):
        """Get the queryset."""
        return super().get_queryset().filter(user=self.request.user)


class StudentAttendanceAdminRetrieveAPIView(RetrieveAPIView):
    """View for retrieving admin student attendance."""

    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = StudentAttendanceAdminRetrieveSerializer
    queryset = StudentAttendance.objects.all()


class TeacherAttendanceAdminListAPIView(ListAPIView):
    """View for listing admin teacher attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = TeacherAttendanceAdminListSerializer
    queryset = TeacherAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = AttendanceFilter

    def get_queryset(self):
        """Get the queryset."""
        return super().get_queryset().filter(user=self.request.user)


class TeacherAttendanceAdminRetrieveAPIView(RetrieveAPIView):
    """View for retrieving admin teacher attendance."""

    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = TeacherAttendanceAdminRetrieveSerializer
    queryset = TeacherAttendance.objects.all()
