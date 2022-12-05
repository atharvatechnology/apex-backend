from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from attendance.api_admin.serializers import (
    StudentAttendanceAdminHistoryListSerializer,
    StudentAttendanceAdminListSerializer,
    StudentAttendanceAdminRetrieveSerializer,
    StudentAttendanceAdminUpdateSerializer,
    TeacherAttendanceAdminHistoryListSerializer,
    TeacherAttendanceAdminListSerializer,
    TeacherAttendanceAdminRetrieveSerializer,
    TeacherAttendanceAdminUpdateSerializer,
)
from attendance.filters import AttendanceFilter
from attendance.models import StudentAttendance, TeacherAttendance
from common.api.views import BaseCreatorUpdateAPIView
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


class StudentAttendanceAdminRetrieveAPIView(RetrieveAPIView):
    """View for retrieving admin student attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentAttendanceAdminRetrieveSerializer
    queryset = StudentAttendance.objects.all()


class StudentAttendanceAdminUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for listing admin student attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentAttendanceAdminUpdateSerializer
    queryset = StudentAttendance.objects.all()


class StudentAttendanceAdminHistoryListAPIView(ListAPIView):
    """View for listing admin student history attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentAttendanceAdminHistoryListSerializer
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


class StudentAttendanceAdminDeleteAPIView(DestroyAPIView):
    """View for deleting admin student attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = StudentAttendance.objects.all()


class TeacherAttendanceAdminListAPIView(ListAPIView):
    """View for listing history of admin teacher attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = TeacherAttendanceAdminListSerializer
    queryset = TeacherAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = AttendanceFilter
    pagination_class = StandardResultsSetPagination


class TeacherAttendanceAdminHistoryListAPIView(ListAPIView):
    """View for listing admin teacher attendance."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = TeacherAttendanceAdminHistoryListSerializer
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


class TeacherAttendanceAdminUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating admin teacher attendanace models."""

    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = TeacherAttendanceAdminUpdateSerializer
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceAdminRetrieveAPIView(RetrieveAPIView):
    """View for retrieving admin teacher attendanace models."""

    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = TeacherAttendanceAdminRetrieveSerializer
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceAdminDeleteAPIView(DestroyAPIView):
    """View for deleting admin teacher attendanace models."""

    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = TeacherAttendance.objects.all()
