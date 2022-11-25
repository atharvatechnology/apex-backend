from rest_framework.generics import ListAPIView, RetrieveAPIView

from common.paginations import StandardResultsSetPagination

from ..models import CourseInfo, CourseInfoCategory, WebResouce
from .serializers import (
    CourseInfoCategoryRetrieveSerializer,
    CourseInfoRetrieveSerializer,
    WebResouceListSerializer,
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


class WebResouceListAPIView(ListAPIView):
    """WebResouce list view."""

    serializer_class = WebResouceListSerializer
    queryset = WebResouce.objects.all()
    pagination_class = StandardResultsSetPagination
    ordering_fields = ["-created_at"]
