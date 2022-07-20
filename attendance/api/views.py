from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from attendance.api.serializers import (
    AttendanceCreateSerializer,
    AttendanceDeleteSerializer,
    AttendanceRetrieveSerializer,
    AttendanceUpdateSerializer,
    TeacherAttendanceCreateSerializer,
    TeacherAttendanceDetailDeleteSerializer,
    TeacherAttendanceDetailRetrieveSerializer,
    TeacherAttendanceDetailUpdateSerializer,
    TeacherAttendanceRetrieveSerializer,
    TeacherAttendanceUpdateSerializer,
)
from attendance.models import Attendance, TeacherAttendance, TeacherAttendanceDetail
from common.api.views import BaseCreatorCreateAPIView
from courses.api.paginations import LargeResultsSetPagination

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


class TeacherAttendanceDetailListAPIView(ListAPIView):
    """View for listing teacher attendance."""

    permission_classes = [AllowAny]
    serializer_class = TeacherAttendanceDetailRetrieveSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating teacher attendance."""

    # permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceCreateSerializer


class TeacherAttendanceRetrieveAPIView(RetrieveAPIView):
    """View for retriving teacher attendance."""

    permission_classes = [AllowAny]
    serializer_class = TeacherAttendanceRetrieveSerializer
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceUpdateAPIView(UpdateAPIView):
    """View for updating teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceUpdateSerializer
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceDetailRetrieveAPIView(RetrieveAPIView):
    """View for retrieving teacher attendance."""

    permission_classes = [AllowAny]
    serializer_class = TeacherAttendanceDetailRetrieveSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceDetailUpdateAPIView(UpdateAPIView):
    """View for updating teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailUpdateSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceDetailDeleteAPIView(DestroyAPIView):
    """View for deleting teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailDeleteSerializer
    queryset = TeacherAttendanceDetail.objects.all()
