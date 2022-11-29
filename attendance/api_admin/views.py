from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from attendance.api_admin.serializers import (
    StudentAttendanceAdminListSerializer,
    TeacherAttendanceAdminListSerializer,
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


class TeacherAttendanceAdminListAPIView(ListAPIView):
    """View for listing admin teacher attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = TeacherAttendanceAdminListSerializer
    queryset = TeacherAttendance.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    filterset_class = AttendanceFilter
