import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

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


class CourseFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Course
        fields = ["price", "category"]


# class CourseFilter(django_filters.FilterSet):
#     class Meta:
#         model = Course
#         fields = {
#             'price': ['lt', 'gt']
#         }


class CourseListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseRetrieveSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    queryset = Course.objects.all()
    filterset_class = CourseFilter


class CourseCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseCreateSerializer


class CourseRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseRetrieveSerializer
    queryset = Course.objects.all()


class CourseUpdateAPIView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseUpdateSerializer

    queryset = Course.objects.all()
    # category_id = self.kwargs.get('catid')
    # if category_id:
    #     return queryset.filter(category=category_id)
    # return queryset


class CourseDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseDeleteSerializer
    queryset = Course.objects.all()


class CourseCategoryListAPIView(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = CourseCategoryRetrieveSerializer
    queryset = CourseCategory.objects.all()
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['name']


class CourseCategoryCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseCategoryCreateSerialilzer


class CourseCategoryRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseCategoryRetrieveSerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryUpdateAPIView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseCategoryUpdateSerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseCategoryDeleteSerializer
    queryset = CourseCategory.objects.all()
