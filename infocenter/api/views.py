from rest_framework.generics import ListAPIView, RetrieveAPIView

from ..models import CourseInfo, CourseInfoCategory
from .serializers import (
    CourseInfoCategoryRetrieveSerializer,
    CourseInfoRetrieveSerializer,
)


class CourseInfoCategoryListAPIView(ListAPIView):
    """CourseInfoCategory list view."""

    serializer_class = CourseInfoCategoryRetrieveSerializer
    queryset = CourseInfoCategory.objects.all()


class CourseInfoCategoryRetrieveAPIView(RetrieveAPIView):
    """CourseInfoCategory retrieve view."""

    serializer_class = CourseInfoCategoryRetrieveSerializer
    queryset = CourseInfoCategory.objects.all()


class CourseInfoListAPIView(ListAPIView):
    """CourseInfo list view."""

    serializer_class = CourseInfoRetrieveSerializer
    queryset = CourseInfo.objects.all()


class CourseInfoRetrieveAPIView(RetrieveAPIView):
    """CourseInfo retrieve view."""

    serializer_class = CourseInfoRetrieveSerializer
    queryset = CourseInfo.objects.all()
