from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from common.paginations import LargeResultsSetPagination
from courses.api.permissions import IsCourseEnrolledActive
from courses.api.serializers import (
    CourseCategoryRetrieveSerializer,
    CourseListSerializer,
    CourseRetrieveSerializerAfterEnroll,
    CourseRetrieveSerializerBeforeEnroll,
)
from courses.filters import CourseFilter
from courses.models import Course, CourseCategory


class CourseListAPIView(ListAPIView):
    """View for listing courses."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    queryset = Course.objects.all()
    filterset_class = CourseFilter
    pagination_class = LargeResultsSetPagination
    # filterset_fields = ['price', 'category']
    # ordering = ['course']


class CourseRetrieveAPIAfterEnrollView(RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [IsAuthenticated, IsCourseEnrolledActive]
    serializer_class = CourseRetrieveSerializerAfterEnroll
    queryset = Course.objects.all()


class CourseRetrieveAPIBeforeEnrollView(RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseRetrieveSerializerBeforeEnroll
    queryset = Course.objects.all()


class CourseCategoryListAPIView(ListAPIView):
    """View for listing course categories."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseCategoryRetrieveSerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryRetrieveAPIView(RetrieveAPIView):
    """View for retrieving course categories."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseCategoryRetrieveSerializer
    queryset = CourseCategory.objects.all()
