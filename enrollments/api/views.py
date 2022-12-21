from django.utils.timezone import localtime
from rest_framework import serializers, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from common.utils import dynamic_excel_generator
from courses.models import Course
from enrollments.api.serializers import (
    CourseEnrollmentRetrieveSerializer,
    CourseEnrollmentSerializer,
    CourseEnrollmentUpdateSerializer,
    CourseExamEnrollmentCreateSerializer,
    EnrollmentCreateSerializer,
    EnrollmentRetrieveSerializer,
    ExamEnrollmentCheckPointRetrieveSerializer,
    ExamEnrollmentRetrievePoolSerializer,
    ExamEnrollmentRetrieveSerializer,
    ExamEnrollmentUpdateSerializer,
    PhysicalBookCourseEnrollmentSerializer,
    PracticeExamEnrollmentCreateSerializer,
    StudentEnrollmentSerializer,
)
from enrollments.models import (
    CourseThroughEnrollment,
    Enrollment,
    EnrollmentStatus,
    ExamEnrollmentStatus,
    ExamThroughEnrollment,
    PhysicalBookCourseEnrollment,
    SessionStatus,
)
from exams.models import Exam


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


class PracticeExamEnrollmentCreateAPIView(CreateAPIView):
    """Create a new practice exam enrollment for a student."""

    permission_classes = [IsAuthenticated]
    serializer_class = PracticeExamEnrollmentCreateSerializer
    queryset = Enrollment.objects.all()

    def perform_create(self, serializer):
        """Create a new practice exam enrollment for the current user.

        Parameters
        ----------
        serializer : PracticeExamEnrollmentCreateSerializer
            Serializer for the enrollment creation.

        Returns
        -------
        Enrollment
            The newly created enrollment.

        """
        return serializer.save(student=self.request.user)


class PracticeEnrollmentCreateAPIView(CreateAPIView):
    """Create or update enrollment of a student for a practice exam."""

    permission_classes = [IsAuthenticated]
    queryset = Enrollment.objects.all()
    serializer_class = PracticeExamEnrollmentCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(student=self.request.user)


class CourseExamEnrollmentCreateAPIView(EnrollmentCreateAPIView):
    """Create a exam enrollment according to course for a student."""

    serializer_class = CourseExamEnrollmentCreateSerializer

    def create(self, request, *args, **kwargs):
        course_id = self.kwargs.get("pk")
        exam_id = self.kwargs.get("exam_id")
        user = self.request.user

        course = Course.objects.get(id=course_id)
        exam = Exam.objects.get(id=exam_id)

        if exam.course == course:
            course_enrollment = Enrollment.objects.filter(
                student=user, courses__in=[course]
            )

            if course_enrollment.exists():
                exam_enrollment = Enrollment.objects.filter(
                    student=user, exams__in=[exam]
                )

                if exam_enrollment.exists():
                    exam_enrollment.delete()

                return super().create(request, *args, **kwargs)
            raise serializers.ValidationError("You are not enrolled in this course")
        raise serializers.ValidationError("Exam does not belong to course")


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
        if exam_enrollment.enrollment.status != EnrollmentStatus.ACTIVE:
            return Response(
                {"detail": "Your enrollment is inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        selected_session = exam_enrollment.selected_session
        if selected_session.is_visible and (
            selected_session.status == SessionStatus.RESULTSOUT
        ):
            # if (selected_session.status == SessionStatus.RESULTSOUT):
            return super().retrieve(request, *args, **kwargs)
        if publish_date := selected_session.result_publish_date:
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

    def get_queryset(self):
        return super().get_queryset().filter(enrollment__student=self.request.user)


class CourseEnrollementUpdateAPIView(UpdateAPIView):
    """Update view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        return (
            super().get_queryset().none()
            if user.is_anonymous
            else super().get_queryset().filter(enrollment__student=user)
        )


class CourseEnrollementRetrieveAPIView(RetrieveAPIView):
    """Retrieve view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentRetrieveSerializer

    def get_queryset(self):
        user = self.request.user
        return (
            super().get_queryset().none()
            if user.is_anonymous
            else super().get_queryset().filter(enrollment__student=user)
        )


class CourseEnrollementDestroyAPIView(DestroyAPIView):
    """Destroy view for course enrollment."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseEnrollmentSerializer
    queryset = CourseThroughEnrollment.objects.all()


class CheckIfStudentInCourse(CreateAPIView):
    serializer_class = StudentEnrollmentSerializer
