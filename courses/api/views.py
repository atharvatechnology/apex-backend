from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from common.api.mixin import InterestWiseOrderMixin, PublishableModelMixin
from common.paginations import StandardResultsSetPagination
from courses.api.permissions import IsCourseEnrolledActive
from courses.api.serializers import (
    CourseCategoryRetrieveSerializer,
    CourseListSerializer,
    CourseRetrieveSerializerAfterEnroll,
    CourseRetrieveSerializerBeforeEnroll,
)
from courses.filters import CourseFilter
from courses.models import Course, CourseCategory
from enrollments.models import CourseThroughEnrollment, Enrollment, SessionStatus


class CourseListAPIView(PublishableModelMixin, InterestWiseOrderMixin, ListAPIView):
    """View for listing courses."""

    permission_classes = [AllowAny]
    serializer_class = CourseListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    queryset = Course.objects.all()
    filterset_class = CourseFilter
    pagination_class = StandardResultsSetPagination
    # filterset_fields = ['price', 'category']
    # ordering = ['course']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class CourseRetrieveAPIAfterEnrollView(PublishableModelMixin, RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [IsAuthenticated, IsCourseEnrolledActive]
    serializer_class = CourseRetrieveSerializerAfterEnroll
    queryset = Course.objects.all()

    def _get_student_enrollment(self, obj):
        if not hasattr(self, "_student_enrollment"):
            try:
                student_enrollment = obj.enrolls.filter(
                    student=self.request.user
                ).latest("id")
            except Enrollment.DoesNotExist:
                student_enrollment = None
            self._student_enrollment = student_enrollment
        return self._student_enrollment

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student_enrollment = self._get_student_enrollment(instance)
        if student_enrollment:
            try:
                student_through_enrollment = (
                    student_enrollment.course_enrolls.select_related(
                        "selected_session"
                    ).latest("id")
                )
            except CourseThroughEnrollment.DoesNotExist:
                student_through_enrollment = None
            request.student_through_enrollment = student_through_enrollment
            session = student_through_enrollment.selected_session
            session_status = session.status
            if session_status == SessionStatus.ACTIVE:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            return Response({"detail": "Course Session is not active"}, status=400)
        return Response(
            f"You do not have any active sessions for {instance.name} course"
        )


class CourseRetrieveAPIBeforeEnrollView(PublishableModelMixin, RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [AllowAny]
    serializer_class = CourseRetrieveSerializerBeforeEnroll
    queryset = Course.objects.all()


class CourseCategoryListAPIView(ListAPIView):
    """View for listing course categories."""

    permission_classes = [AllowAny]
    serializer_class = CourseCategoryRetrieveSerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryRetrieveAPIView(RetrieveAPIView):
    """View for retrieving course categories."""

    permission_classes = [AllowAny]
    serializer_class = CourseCategoryRetrieveSerializer
    queryset = CourseCategory.objects.all()
