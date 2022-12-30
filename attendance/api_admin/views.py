from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView

from attendance.api_admin.serializers import (
    StudentAttendanceAdminHistoryListSerializer,
    StudentAttendanceAdminListSerializer,
    StudentAttendanceAdminRetrieveSerializer,
    StudentAttendanceAdminUpdateSerializer,
    TeacherAttendanceAdminListSerializer,
    TeacherAttendanceAdminRetrieveSerializer,
    TeacherAttendanceAdminUpdateSerializer,
    TeacherAttendanceDetailAdminSerializer,
)
from attendance.filters import AttendanceFilter
from attendance.models import (
    StudentAttendance,
    TeacherAttendance,
    TeacherAttendanceDetail,
)
from common.api.views import BaseCreatorUpdateAPIView
from common.paginations import StandardResultsSetPagination
from common.permissions import IsAdminorSuperAdminorDirector


class StudentAttendanceAdminListAPIView(ListAPIView):
    """View for listing admin student attendance."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = StudentAttendanceAdminListSerializer
    queryset = StudentAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    filterset_class = AttendanceFilter
    pagination_class = StandardResultsSetPagination


class StudentAttendanceAdminRetrieveAPIView(RetrieveAPIView):
    """View for retrieving admin student attendance."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = StudentAttendanceAdminRetrieveSerializer
    queryset = StudentAttendance.objects.all()


class StudentAttendanceAdminUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for listing admin student attendance."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = StudentAttendanceAdminUpdateSerializer
    queryset = StudentAttendance.objects.all()


class StudentAttendanceAdminHistoryListAPIView(ListAPIView):
    """View for listing admin student history attendance."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = StudentAttendanceAdminHistoryListSerializer
    queryset = StudentAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = AttendanceFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get the queryset."""
        if student_id := self.kwargs.get("student_id", None):
            return super().get_queryset().filter(user=student_id)
        else:
            raise ValidationError("Student id is required.")


class StudentAttendanceAdminDeleteAPIView(DestroyAPIView):
    """View for deleting admin student attendance."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    queryset = StudentAttendance.objects.all()


class TeacherAttendanceAdminListAPIView(ListAPIView):
    """View for listing history of admin teacher attendance."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = TeacherAttendanceAdminListSerializer
    queryset = TeacherAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    filterset_class = AttendanceFilter
    pagination_class = StandardResultsSetPagination


class TeacherAttendanceAdminHistoryListAPIView(ListAPIView):
    """View for listing admin teacher attendance."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = TeacherAttendanceAdminListSerializer
    queryset = TeacherAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = AttendanceFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get the queryset."""
        if teacher_id := self.kwargs.get("teacher_id", None):
            return super().get_queryset().filter(user=teacher_id)
        else:
            raise ValidationError("Teacher id is required.")


class TeacherAttendanceAdminUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating admin teacher attendanace."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = TeacherAttendanceAdminUpdateSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceAdminRetrieveAPIView(RetrieveAPIView):
    """View for retrieving admin teacher attendanace."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = TeacherAttendanceAdminRetrieveSerializer
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceAdminDeleteAPIView(DestroyAPIView):
    """View for deleting admin teacher attendanace."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceDetailAdminListAPIView(ListAPIView):
    """View for listing admin teacher attendance detail."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = TeacherAttendanceDetailAdminSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    queryset = TeacherAttendanceDetail.objects.all()

    def get_queryset(self):
        """Get the queryset."""
        if teacher_attendance_id := self.kwargs.get("attendance_id", None):
            return (
                super()
                .get_queryset()
                .filter(teacher_attendance_id=teacher_attendance_id)
            )
        else:
            raise ValidationError("Teacher attendance id is required.")


class TeacherAttendanceDetailAdminRetrieveAPIView(RetrieveAPIView):
    """View for retrieving admin teacher attendance detail."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = TeacherAttendanceDetailAdminSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceDetailAdminUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating admin teacher attendance detail."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = TeacherAttendanceDetailAdminSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceDetailAdminDeleteAPIView(DestroyAPIView):
    """View for deleting admin teacher attendance detail."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = TeacherAttendanceDetailAdminSerializer
    queryset = TeacherAttendanceDetail.objects.all()
