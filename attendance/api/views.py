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
    TeacherAttendanceDetailSerializer,
    TeacherAttendanceRetrieveSerializer,
)
from attendance.filters import AttendanceFilter
from attendance.models import (
    StudentAttendance,
    TeacherAttendance,
    TeacherAttendanceDetail,
)
from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView

# from common.paginations import StandardResultsSetPagination
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
    # pagination_class = StandardResultsSetPagination

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

    def perform_create(self, serializer):
        """Save serializer object with current user as user, check existing attendance.

        Args:
            serializer: The serializer object.

        Raises
            ValidationError: If attendance for user on the given date already exists.

        Returns
            None

        """
        # Set the user of the serializer to the current user
        user = self.request.user
        date = self.request.data.get("date").split("T")[0]
        if StudentAttendance.objects.filter(user=user, date__date=date).exists():
            raise ValidationError("Attendance already exists")

        serializer.save(
            user=user,
            created_by=user,
            updated_by=user,
        )


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
    filterset_class = AttendanceFilter
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TeacherAttendanceCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating teacher attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceCreateSerializer

    def perform_create(self, serializer):
        """Save serializer object with current user as user, check existing attendance.

        Args:
            serializer: The serializer object.

        Raises
            ValidationError: If attendance for user on the given date already exists.

        Returns
            None

        """
        # Set the user of the serializer to the current user
        user = self.request.user
        date = self.request.data.get("date").split("T")[0]
        if TeacherAttendance.objects.filter(user=user, date__date=date).exists():
            raise ValidationError("Attendance already exists")

        serializer.save(
            user=user,
            created_by=user,
            updated_by=user,
        )


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
        """Get appropriate serializer class based on scanned user from QR code.

        Returns
            Serializer class: based on the user scanned from the QR code.

        Raises
            ValidationError: If user is not found or not a student/teacher.

        """
        # Decode the user scanned from the QR code
        decoded_user = None
        if user := self.request.data.get("user"):
            decoded_user = decode_user(user)

        # Find the user object from the decoded username
        user_object = None
        if decoded_user is not None:
            user_object = User.objects.filter(username=decoded_user).first()

        # For Swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return StudentAttendanceCreateSerializer

        # Raise an error if the user is not found or is not a student or teacher
        if not user_object:
            raise ValidationError("User doesn't exists.")
        if user_object.is_student:
            return StudentAttendanceCreateSerializer
        elif user_object.is_teacher:
            return TeacherAttendanceCreateSerializer
        raise ValidationError("Qr code is not valid.")


class TeacherAttendanceDetailCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating teacher detail attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailCreateSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceDetailListAPIView(ListAPIView):
    """View for listing teacher detail attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailSerializer
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
    serializer_class = TeacherAttendanceDetailSerializer
    queryset = TeacherAttendanceDetail.objects.all()


class TeacherAttendanceDetailUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating teacher detail attendance."""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherAttendanceDetailSerializer
    queryset = TeacherAttendanceDetail.objects.all()
