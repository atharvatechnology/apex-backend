from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from attendance.api.paginations import LargeResultsSetPagination
from attendance.api.serializers import (
    AttendanceCreateSerializer,
    AttendanceDeleteSerializer,
    AttendanceRetrieveSerializer,
    AttendanceUpdateSerializer,
    TeacherAttendanceDetailCreateSerializer,
    TeacherAttendanceDetailDeleteSerializer,
    TeacherAttendanceDetailRetrieveSerializer,
    TeacherAttendanceDetailUpdateSerializer,
)
from attendance.models import Attendance, TeacherAttendance
from common.api.views import BaseCreatorCreateAPIView

from ..filters import AttendanceFilter


class AttendanceListAPIView(ListAPIView):
    """View for listing attendance."""

    permission_classes = [AllowAny]
    serializer_class = AttendanceRetrieveSerializer
    queryset = Attendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = AttendanceFilter
    pagination_class = LargeResultsSetPagination


class AttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating attendance."""

    # permission_classes = [IsAuthenticated]
    serializer_class = AttendanceCreateSerializer


class AttendanceRetrieveAPIView(RetrieveAPIView):
    """View for retrieving attendance."""

    permission_classes = [AllowAny]
    serializer_class = AttendanceRetrieveSerializer
    queryset = Attendance.objects.all()


class AttendanceUpdateAPIView(UpdateAPIView):
    """View for updating attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceUpdateSerializer
    queryset = Attendance.objects.all()


class AttendanceDeleteAPIView(DestroyAPIView):
    """View for deleting attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceDeleteSerializer
    queryset = Attendance.objects.all()


class TeacherAttendanceListAPIView(ListAPIView):
    """View for listing teacher attendance."""

    permission_classes = [AllowAny]
    serializer_class = TeacherAttendanceDetailRetrieveSerializer
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating teacher attendance."""

    # permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailCreateSerializer


class TeacherAttendanceRetrieveAPIView(RetrieveAPIView):
    """View for retrieving teacher attendance."""

    permission_classes = [AllowAny]
    serializer_class = TeacherAttendanceDetailRetrieveSerializer
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceUpdateAPIView(UpdateAPIView):
    """View for updating teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailUpdateSerializer
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceDeleteAPIView(DestroyAPIView):
    """View for deleting teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailDeleteSerializer
    queryset = TeacherAttendance.objects.all()
