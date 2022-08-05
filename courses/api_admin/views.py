from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from common.paginations import LargeResultsSetPagination
from courses.api_admin.serializers import CourseCategorySerializer, CourseSerializer
from courses.models import Course, CourseCategory


class CourseCategoryCreateAPIView(CreateAPIView):
    """View for creating course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseCategorySerializer


class CourseCategoryListAPIView(ListAPIView):
    """View for listing course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryRetrieveAPIView(RetrieveAPIView):
    """View for retrieving course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryUpdateAPIView(UpdateAPIView):
    """View for updating course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryDeleteAPIView(DestroyAPIView):
    """View for deleting course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CourseCategory.objects.all()


class CourseCreateAPIView(CreateAPIView):
    """View for creating courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseSerializer


class CourseListAPIView(ListAPIView):
    """View for listing courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LargeResultsSetPagination


class CourseRetrieveAPIView(RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseUpdateAPIView(UpdateAPIView):
    """View for updating courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseDeleteAPIView(DestroyAPIView):
    """View for deleting courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Course.objects.all()
