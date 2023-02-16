from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from common.paginations import StandardResultsSetPagination

from ..models import CourseInfo, CourseInfoCategory, WebResource
from .serializers import (
    CourseInfoCategoryRetrieveSerializer,
    CourseInfoRetrieveSerializer,
    WebResourceListSerializer,
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


class WebResourceListAPIView(ListAPIView):
    """WebResource list view."""

    serializer_class = WebResourceListSerializer
    queryset = WebResource.objects.all()
    pagination_class = StandardResultsSetPagination


@api_view(["GET"])
def get_counts(request):
    """Get counts of all different models."""
    from courses.models import Course
    from exams.models import Exam

    models = [Exam, Course, WebResource]
    counts = {}

    for model in models:
        counts[model.__name__] = model.objects.count()
    return Response(counts, content_type="application/json")
