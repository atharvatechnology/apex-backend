from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.api.paginations import LargeResultsSetPagination
from courses.api.serializers import (
    CourseCategoryCreateSerialilzer,
    CourseCategoryDeleteSerializer,
    CourseCategoryRetrieveSerializer,
    CourseCategoryUpdateSerializer,
    CourseCreateSerializer,
    CourseDeleteSerializer,
    CourseRetrieveSerializer,
    CourseUpdateSerializer,
)
from courses.models import Course, CourseCategory

from ..filters import CourseFilter


class CourseListAPIView(ListAPIView):
    """View for listing courses."""

    permission_classes = [AllowAny]
    serializer_class = CourseRetrieveSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    queryset = Course.objects.all()
    filterset_class = CourseFilter
    pagination_class = LargeResultsSetPagination
    # filterset_fields = ['price', 'category']
    # ordering = ['course']


class CourseCreateAPIView(CreateAPIView):
    """View for creating courses."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseCreateSerializer


class CourseRetrieveAPIView(RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [AllowAny]
    serializer_class = CourseRetrieveSerializer
    queryset = Course.objects.all()


class CourseUpdateAPIView(UpdateAPIView):
    """View for updating courses."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseUpdateSerializer
    queryset = Course.objects.all()


class CourseDeleteAPIView(DestroyAPIView):
    """View for deleting courses."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseDeleteSerializer
    queryset = Course.objects.all()


class CourseCategoryListAPIView(ListAPIView):
    """View for listing course categories."""

    permission_classes = [AllowAny]
    serializer_class = CourseCategoryRetrieveSerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryCreateAPIView(CreateAPIView):
    """View for creating course categories."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseCategoryCreateSerialilzer


class CourseCategoryRetrieveAPIView(RetrieveAPIView):
    """View for retrieving course categories."""

    permission_classes = [AllowAny]
    serializer_class = CourseCategoryRetrieveSerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryUpdateAPIView(UpdateAPIView):
    """View for updating course categories."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseCategoryUpdateSerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryDeleteAPIView(DestroyAPIView):
    """View for deleting course categories."""

    permission_classes = [IsAuthenticated]
    serializer_class = CourseCategoryDeleteSerializer
    queryset = CourseCategory.objects.all()
