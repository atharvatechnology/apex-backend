from datetime import datetime, timedelta, timezone

from django.utils.timezone import localtime
from rest_framework import serializers, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
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
    CourseIdSerializer,
    EnrollmentCreateSerializer,
    EnrollmentRetrieveSerializer,
    ExamEnrollmentCheckPointRetrieveSerializer,
    ExamEnrollmentRetrievePoolSerializer,
    ExamEnrollmentRetrieveSerializer,
    ExamEnrollmentUpdateSerializer,
    PracticeExamEnrollmentCreateSerializer,
    StudentEnrollmentSerializer,
)
from enrollments.models import (  # PhysicalBookCourseEnrollment,
    CourseThroughEnrollment,
    Enrollment,
    EnrollmentStatus,
    ExamEnrollmentStatus,
    ExamThroughEnrollment,
    SessionStatus,
)
from exams.models import Exam
from meetings.api.serializers import MeetingCourseSessionSerializer
from meetings.models import Meeting


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
            serializer = self.get_serializer(exam_enrollment)
            return Response(serializer.data)

        return Response(
            {"detail": "Exam is not active or u have already submitted."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ExamEnrollmentRetrievePoolAPIView(RetrieveAPIView):
    """Retrieve an exam enrollment result."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentRetrievePoolSerializer


# class PhysicalBookCourseEnrollmentListAPIView(ListAPIView):
#     """Physical book list after user course enrolled."""

#     queryset = PhysicalBookCourseEnrollment.objects.all()
#     serializer_class = PhysicalBookCourseEnrollmentSerializer


# class PhysicalBookCourseEnrollmentCreateAPIView(CreateAPIView):
#     """Create physical book after course enrollment."""

#     permission_classes = [IsAuthenticated]
#     queryset = PhysicalBookCourseEnrollment.objects.all()
#     serializer_class = PhysicalBookCourseEnrollmentSerializer


# class PhysicalBookCourseEnrollmentRetrieveAPIView(RetrieveAPIView):
#     """Retrieve physical book after course enrollment."""

#     permission_classes = [IsAuthenticated]
#     queryset = PhysicalBookCourseEnrollment.objects.all()
#     serializer_class = PhysicalBookCourseEnrollmentSerializer


# class PhysicalBookCourseEnrollmentUpdateAPIView(UpdateAPIView):
#     """Update physical book after course enrollment."""

#     permission_classes = [IsAuthenticated]
#     queryset = PhysicalBookCourseEnrollment.objects.all()
#     serializer_class = PhysicalBookCourseEnrollmentSerializer


# class PhysicalBookCourseEnrollmentDestroyAPIView(DestroyAPIView):
#     """Destroy physical book after course enrollment."""

#     permission_classes = [IsAuthenticated]
#     queryset = PhysicalBookCourseEnrollment.objects.all()
#     serializer_class = PhysicalBookCourseEnrollmentSerializer


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


class StudentEnrollmentDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseIdSerializer
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        course_id = self.get_object().id

        course = Course.objects.get(id=course_id)
        course_duration = course.duration.days

        # All classes count
        get_all_meetings = Meeting.objects.filter(course_session__course__id=course_id)
        if get_all_meetings:
            total_classes_count = 0
            for classes in get_all_meetings:
                if classes.repeat_type == 1:
                    duration = course_duration // 1
                elif classes.repeat_type == 2:
                    duration = course_duration // 7
                elif classes.repeat_type == 3:
                    duration = course_duration // 30

                total_classes_count += duration / classes.repeat_interval

        # All exam sessions count
        all_exams = course.exams_exam_related.all()

        # class attended count.
        class_attended_count = (
            CourseThroughEnrollment.objects.filter(course=course_id)
            .filter(enrollment__student=self.request.user.id)
            .first()
        )

        # Exam attempted count by Enrolled Student choosing particular course.
        exam_attempted_count = 0
        for exams in all_exams:
            for exam_enroll in exams.exam_enrolls.filter(
                enrollment__student_id=request.user.id
            ):
                if exam_enroll.question_state.all() > 0:
                    exam_attempted_count += 1

        data = {
            "total_classes_in_course": total_classes_count,
            "total_exams_in_course": all_exams.count(),
            "exam_attempted_count": exam_attempted_count,
            "class_attended_count": class_attended_count.attended_count
            if class_attended_count
            else 0,
        }
        return Response(
            data,
        )


class StudentAttendanceIncrement(GenericAPIView):
    serializer_class = MeetingCourseSessionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_session_id = serializer.data.get("course_session")
        course_through_enrollment = (
            CourseThroughEnrollment.objects.filter(selected_session=course_session_id)
            .filter(enrollment__student=self.request.user.id)
            .first()
        )

        if course_through_enrollment.class_meet_updated:
            time_difference = (
                datetime.now(timezone.utc)
                + timedelta(hours=5, minutes=45)
                - course_through_enrollment.class_meet_updated
            )
            if time_difference.total_seconds() >= 10800:
                course_through_enrollment.attended_count += 1
                course_through_enrollment.save()
                return Response(
                    {"msg": "Congratulations your attendance has been recorded."}
                )

            return Response(
                {"msg": "Your attendance for this session has already been recorded."}
            )
        else:
            course_through_enrollment.attended_count += 1
            course_through_enrollment.save()
            return Response(
                {"msg": "Congratulations your attendance has been recorded."}
            )

        return Response({"msg": "No Course through Enrollment found."})
