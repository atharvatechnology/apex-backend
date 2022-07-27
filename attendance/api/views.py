from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from attendance.api.serializers import (
    AttendanceCreateSerializer,
    AttendanceRetrieveSerializer,
    AttendanceUpdateSerializer,
    TeacherAttendanceCreateSerializer,
    TeacherAttendanceRetrieveSerializer,
    TeacherAttendanceUpdateSerializer,
)
from attendance.filters import AttendanceFilter
from attendance.models import Attendance, TeacherAttendance, TeacherAttendanceDetail
from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from courses.api.paginations import LargeResultsSetPagination


class AttendanceListAPIView(ListAPIView):
    """View for listing attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceRetrieveSerializer
    queryset = Attendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = AttendanceFilter
    pagination_class = LargeResultsSetPagination


class AttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceCreateSerializer


class AttendanceRetrieveAPIView(RetrieveAPIView):
    """View for retrieving attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceRetrieveSerializer
    queryset = Attendance.objects.all()


class AttendanceUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceUpdateSerializer
    queryset = Attendance.objects.all()


class TeacherAttendanceListAPIView(ListAPIView):
    """View for listing teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceRetrieveSerializer
    queryset = TeacherAttendanceDetail.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]


class TeacherAttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceCreateSerializer


class TeacherAttendanceRetrieveAPIView(RetrieveAPIView):
    """View for retriving teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceRetrieveSerializer
    queryset = TeacherAttendance.objects.all()


class TeacherAttendanceUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceUpdateSerializer
    queryset = TeacherAttendance.objects.all()


# class TeacherAttendanceDetailRetrieveAPIView(RetrieveAPIView):
#     """View for retrieving teacher attendance."""

#     permission_classes = [AllowAny]
#     serializer_class = TeacherAttendanceDetailRetrieveSerializer
#     queryset = TeacherAttendanceDetail.objects.all()


# class TeacherAttendanceDetailUpdateAPIView(UpdateAPIView):
#     """View for updating teacher attendance."""

#     permission_classes = [IsAuthenticated]
#     serializer_class = TeacherAttendanceDetailUpdateSerializer
#     queryset = TeacherAttendanceDetail.objects.all()


# class TeacherAttendanceDetailDeleteAPIView(DestroyAPIView):
#     """View for deleting teacher attendance."""

#     permission_classes = [IsAuthenticated]
#     serializer_class = TeacherAttendanceDetailDeleteSerializer
#     queryset = TeacherAttendanceDetail.objects.all()
