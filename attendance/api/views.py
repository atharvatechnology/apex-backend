from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from attendance.api.serializers import (
    AttendanceCreateSerializer,
    StudentAttendanceCreateSerializer,
    StudentAttendanceRetrieveSerializer,
    StudentOnlineAttendanceSerializer,
    TeacherAttendanceCreateSerializer,
    TeacherAttendanceDetailCreateSerializer,
    TeacherAttendanceDetailListSerializer,
    TeacherAttendanceDetailRetrieveSerializer,
    TeacherAttendanceDetailUpdateSerializer,
    TeacherAttendanceRetrieveSerializer,
)
from attendance.filters import AttendanceFilter
from attendance.models import (
    StudentAttendance,
    TeacherAttendance,
    TeacherAttendanceDetail,
)
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


class StudentOnlineAttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentOnlineAttendanceSerializer


class StudentAttendanceRetrieveAPIView(RetrieveAPIView):
    """View for retrieving attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentAttendanceRetrieveSerializer
    queryset = StudentAttendance.objects.all()


class TeacherAttendanceListAPIView(ListAPIView):
    """View for listing teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceRetrieveSerializer
    queryset = TeacherAttendance.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    # filterset_class = AttendanceFilter

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


class AttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceCreateSerializer

    def get_serializer_class(self):
        """Get the serializer class."""
        decoded_user = None
        if user := self.request.data.get("user"):
            decoded_user = decode_user(user)
        user_object = None
        if decoded_user is not None:
            user_object = User.objects.filter(username=decoded_user).first()
        if user_object:
            if user_object.is_student:
                return StudentAttendanceCreateSerializer
            elif user_object.is_teacher:
                return TeacherAttendanceCreateSerializer
        return self.serializer_class


class TeacherAttendanceDetailCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating teacher detail attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailCreateSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceDetailListAPIView(ListAPIView):
    """View for listing teacher detail attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    queryset = TeacherAttendanceDetail.objects.all()

    def get_queryset(self):
        """Get the queryset."""
        if teacher_attendance__id := self.kwargs.get("teacher_attendance_id", None):
            return (
                super()
                .get_queryset()
                .filter(teacher_attendance__id=teacher_attendance__id)
            )
        else:
            raise ValidationError("Teacher attendance id is required.")

    # def get_queryset(self):
    #     """Get the queryset."""
    #     return super().get_queryset().filter(teacher_attendance__id=self.request.user)


class TeacherAttendanceDetailRetrieveAPIView(RetrieveAPIView):
    """View for retrieving teacher detail attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailRetrieveSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceDetailUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating teacher detail attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailUpdateSerializer
    queryset = TeacherAttendanceDetail.objects.all()
