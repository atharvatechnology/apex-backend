from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView
from enrollments.api.serializers import (
    EnrollmentCreateSerializer,
    EnrollmentRetrieveSerializer,
    ExamEnrollmentRetrieveSerializer,
    ExamEnrollmentUpdateSerializer,
    SessionSerializer,
)
from enrollments.models import Enrollment, ExamThroughEnrollment


class SessionCreateAPIView(BaseCreatorCreateAPIView):
    """Create a new session for an exam."""

    serializer_class = SessionSerializer


class EnrollmentCreateAPIView(CreateAPIView):
    """Create a new enrollment for a student."""

    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentCreateSerializer
    queryset = Enrollment.objects.all()

    def perform_create(self, serializer):
        """Create a new enrollment for the current user.

        Parameters
        ----------
        serializer : EnrollmentCreateSerializer
            Serializer for the enrollment creation.

        Returns
        -------
        Enrollment
            The newly created enrollment.

        """
        return serializer.save(student=self.request.user)


class EnrollmentListAPIView(ListAPIView):
    """List all enrollments for a student."""

    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentRetrieveSerializer
    queryset = Enrollment.objects.all()

    def get_queryset(self):
        """Get the enrollments for the current user.

        Returns
        -------
        QuerySet
            The set of enrollments of the current user.

        """
        queryset = super().get_queryset()
        return queryset.filter(student=self.request.user)


class ExamEnrollmentUpdateAPIView(UpdateAPIView):
    """Submit an exam enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentUpdateSerializer


class ExamEnrollmentRetrieveAPIView(RetrieveAPIView):
    """Retrieve an exam enrollment result."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentRetrieveSerializer
