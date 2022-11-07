from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from common.paginations import StandardResultsSetPagination
from enrollments.api_admin.serializers import (
    CourseEnrollmentCreateSerializer,
    CourseSessionAdminSerializer,
    CourseSessionAdminUpdateSerializer,
    CourseThroughEnrollmentAdminBaseSerializer,
    ExamEnrollmentCreateSerializer,
    ExamSessionAdminSerializer,
    ExamSessionAdminUpdateSerializer,
    ExamThroughEnrollmentAdminListSerializer,
    StudentEnrollmentCheckSerializer,
)
from enrollments.filters import (
    CourseThroughEnrollmentFilter,
    ExamThroughEnrollmentFilter,
)
from enrollments.models import (
    CourseSession,
    CourseThroughEnrollment,
    Enrollment,
    ExamSession,
    ExamThroughEnrollment,
)


class ExamSessionCreateAPIView(BaseCreatorCreateAPIView):
    """Create a new session for an exam."""

    serializer_class = ExamSessionAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ExamSessionUpdateAPIView(BaseCreatorUpdateAPIView):
    """Update an existing session for an exam."""

    serializer_class = ExamSessionAdminUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ExamSession.objects.all()

    def can_update_object(self, obj):
        """Check if the user can update the object.

        Raises a PermissionDenied exception
            if the user cannot update a session which is ended.
        """
        if obj.end_date < timezone.now():
            self.permission_denied(
                self.request, message="Cannot update a session which is ended."
            )

    def get_object(self):
        obj = super().get_object()
        self.can_update_object(obj)
        return obj


class ExamSessionListAPIView(ListAPIView):
    """List all sessions for an exam."""

    serializer_class = ExamSessionAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ExamSession.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(exam__id=self.kwargs["exam_id"])


class ExamSessionDeleteAPIView(DestroyAPIView):
    """Delete an existing session for an exam."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ExamSession.objects.all()

    def can_delete(self, object):
        """Check if the user can delete the object.

        Raises a PermissionDenied exception
            if the user cannot delete a session which is ended.
        """
        if object.start_date < timezone.now():
            self.permission_denied(
                self.request,
                message="Cannot delete a session that has already started.",
            )

    def get_object(self):
        obj = super().get_object()
        self.can_delete(obj)
        return obj


# Course Session starts


class CourseSessionCreateAPIView(BaseCreatorCreateAPIView):
    """Create a new session for an exam."""

    serializer_class = CourseSessionAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class CourseSessionUpdateAPIView(BaseCreatorUpdateAPIView):
    """Update an existing session for an exam."""

    serializer_class = CourseSessionAdminUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CourseSession.objects.all()

    def can_update_object(self, obj):
        """Check if the user can update the object.

        Raises a PermissionDenied exception
            if the user cannot update a session which is ended.
        """
        if obj.end_date < timezone.now():
            self.permission_denied(
                self.request, message="Cannot update a session which is ended."
            )

    def get_object(self):
        obj = super().get_object()
        self.can_update_object(obj)
        return obj


class CourseSessionListAPIView(ListAPIView):
    """List all sessions for an exam."""

    serializer_class = CourseSessionAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CourseSession.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(course__id=self.kwargs["course_id"])


class CourseSessionDeleteAPIView(DestroyAPIView):
    """Delete an existing session for an exam."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CourseSession.objects.all()

    def can_delete(self, object):
        """Check if the user can delete the object.

        Raises a PermissionDenied exception
            if the user cannot delete a session which is ended.
        """
        if object.start_date < timezone.now():
            self.permission_denied(
                self.request,
                message="Cannot delete a session that has already started.",
            )

    def get_object(self):
        obj = super().get_object()
        self.can_delete(obj)
        return obj


# course session ends


class ExamEnrollmentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ExamEnrollmentCreateSerializer
    queryset = Enrollment.objects.all()


class CourseEnrollmentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseEnrollmentCreateSerializer
    queryset = Enrollment.objects.all()


class ExamThroughEnrollmentListAPIView(ListAPIView):
    """List all student in Exam."""

    serializer_class = ExamThroughEnrollmentAdminListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ExamThroughEnrollment.objects.order_by("-score")
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    pagination_class = StandardResultsSetPagination
    search_fields = [
        "enrollment__student__first_name",
        "enrollment__student__last_name",
        "enrollment__student__username",
        "exam__name",
    ]
    ordering_fields = ["status", "score"]
    filterset_class = ExamThroughEnrollmentFilter


class CourseThroughEnrollmentListAPIView(ListAPIView):
    """List all student in Course."""

    serializer_class = CourseThroughEnrollmentAdminBaseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CourseThroughEnrollment.objects.order_by("-enrollment__created_at")
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    pagination_class = StandardResultsSetPagination
    search_fields = [
        "enrollment__student__first_name",
        "enrollment__student__last_name",
        "enrollment__student__username",
        "course__name",
    ]
    # ordering_fields = ["status", "score"]
    filterset_class = CourseThroughEnrollmentFilter


class StudentCourseCheckView(GenericAPIView):
    """View for checking if student is enrolled in a course."""

    permission_classes = []
    serializer_class = StudentEnrollmentCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"status": "success", "message": "Student is enrolled in the course."}
        )
