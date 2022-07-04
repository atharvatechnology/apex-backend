from django.utils.timezone import localtime
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from enrollments.api.serializers import (
    CourseEnrollmentRetrieveSerializer,
    CourseEnrollmentSerializer,
    CourseEnrollmentUpdateSerializer,
    EnrollmentCreateSerializer,
    EnrollmentRetrieveSerializer,
    ExamEnrollmentCheckPointRetrieveSerializer,
    ExamEnrollmentRetrievePoolSerializer,
    ExamEnrollmentRetrieveSerializer,
    ExamEnrollmentUpdateSerializer,
    PhysicalBookCourseEnrollmentSerializer,
)
from enrollments.models import (
    CourseThroughEnrollment,
    Enrollment,
    ExamEnrollmentStatus,
    ExamThroughEnrollment,
    PhysicalBookCourseEnrollment,
    SessionStatus,
)


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

    def update(self, request, *args, **kwargs):
        exam_enrollment = self.get_object()
        if exam_enrollment.status != ExamEnrollmentStatus.CREATED:
            return Response(
                {"detail": "Your answers have already been submitted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)


class ExamEnrollmentRetrieveAPIView(RetrieveAPIView):
    """Retrieve an exam enrollment result."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        exam_enrollment = self.get_object()
        # if (
        #     # the exam is still in progress
        #     exam_enrollment.selected_session.status
        #     == SessionStatus.ENDED
        # ) and (
        #     # the exam result has not been calculated yet
        #     exam_enrollment.status
        #     in [ExamEnrollmentStatus.FAILED, ExamEnrollmentStatus.PASSED]
        # ):
        selected_session = exam_enrollment.selected_session
        if selected_session.is_visible and (
            selected_session.status == SessionStatus.RESULTSOUT
        ):
            # if (selected_session.status == SessionStatus.RESULTSOUT):
            return super().retrieve(request, *args, **kwargs)
        if publish_date := selected_session.publish_date:
            error_detail = f"Your result will be published \
                on {localtime(publish_date).strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            error_detail = "Your result has not been published yet."

        return Response(
            {"detail": error_detail},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ExamEnrollmentCheckpointRetrieveAPIView(RetrieveAPIView):
    """Retrieve an exam enrollment saved state."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentCheckPointRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        exam_enrollment = self.get_object()
        if (
            # the exam is still in progress
            exam_enrollment.selected_session.status
            == SessionStatus.ACTIVE
        ) and (
            # the exam result has not been calculated yet
            exam_enrollment.status
            in [ExamEnrollmentStatus.CREATED]
        ):
            return super().retrieve(request, *args, **kwargs)

        return Response(
            {"detail": "Exam is not active or u have already submitted."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ExamEnrollmentRetrievePoolAPIView(RetrieveAPIView):
    """Retrieve an exam enrollment result."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentRetrievePoolSerializer


class PhysicalBookCourseEnrollmentListAPIView(ListAPIView):
    """Physical book list after user course enrolled."""

    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class PhysicalBookCourseEnrollmentCreateAPIView(CreateAPIView):
    """Create physical book after course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class PhysicalBookCourseEnrollmentRetrieveAPIView(RetrieveAPIView):
    """Retrieve physical book after course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class PhysicalBookCourseEnrollmentUpdateAPIView(UpdateAPIView):
    """Update physical book after course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class PhysicalBookCourseEnrollmentDestroyAPIView(DestroyAPIView):
    """Destroy physical book after course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class CourseEnrollementListAPIView(ListAPIView):
    """List view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer


class CourseEnrollementCreateAPIView(CreateAPIView):
    """create view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer


class CourseEnrollementUpdateAPIView(UpdateAPIView):
    """Update view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentUpdateSerializer


class CourseEnrollementRetrieveAPIView(RetrieveAPIView):
    """Retrieve view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentRetrieveSerializer


class CourseEnrollementDestroyAPIView(DestroyAPIView):
    """Destroy view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
