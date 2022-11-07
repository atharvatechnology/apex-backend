from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from attendance.api.serializers import (
    AttendanceCreateSerializer,
    StudentAttendanceCreateSerializer,
    StudentAttendanceRetrieveSerializer,
    StudentAttendanceUpdateSerializer,
    TeacherAttendanceCreateSerializer,
    TeacherAttendanceRetrieveSerializer,
    TeacherAttendanceUpdateSerializer,
)
from attendance.filters import AttendanceFilter
from attendance.models import StudentAttendance, TeacherAttendance
from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from common.paginations import StandardResultsSetPagination
from common.utils import decode_user

User = get_user_model()


class StudentAttendanceListAPIView(ListAPIView):
    """View for listing attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentAttendanceRetrieveSerializer
    queryset = StudentAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = AttendanceFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get the queryset."""
        return super().get_queryset().filter(user=self.request.user)


class StudentAttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentAttendanceCreateSerializer


class StudentAttendanceRetrieveAPIView(RetrieveAPIView):
    """View for retrieving attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentAttendanceRetrieveSerializer
    queryset = StudentAttendance.objects.all()


class StudentAttendanceUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentAttendanceUpdateSerializer
    queryset = StudentAttendance.objects.all()


class TeacherAttendanceListAPIView(ListAPIView):
    """View for listing teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceRetrieveSerializer
    queryset = TeacherAttendance.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


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


class AttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceCreateSerializer

    def get_serializer_class(self):
        """Get the serializer class."""
        user = self.request.data.get("user")
        decoded_user = decode_user(user)
        user_object = None
        if decoded_user is not None:
            user_object = User.objects.filter(username=decoded_user).first()
        if user_object and user_object.is_student:
            return StudentAttendanceCreateSerializer
        elif user_object and user_object.is_teacher:
            return TeacherAttendanceCreateSerializer
        else:
            return AttendanceCreateSerializer


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
