from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from common.paginations import StandardResultsSetPagination
from courses.api.serializers import (
    CourseCategoryRetrieveSerializer,
    CourseRetrieveSerializerAfterEnroll,
    CourseRetrieveSerializerBeforeEnroll,
)
from courses.models import Course, CourseCategory

from ..filters import CourseFilter


class CourseListAPIView(ListAPIView):
    """View for listing courses."""

    permission_classes = [AllowAny]
    serializer_class = CourseRetrieveSerializerAfterEnroll
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    queryset = Course.objects.all()
    filterset_class = CourseFilter
    pagination_class = StandardResultsSetPagination
    # filterset_fields = ['price', 'category']
    # ordering = ['course']


class CourseRetrieveAPIViewBeforeEnroll(RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [AllowAny]
    serializer_class = CourseRetrieveSerializerBeforeEnroll
    queryset = Course.objects.all()


class CourseRetrieveAPIViewAfterEnroll(RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [AllowAny]
    serializer_class = CourseRetrieveSerializerAfterEnroll
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
