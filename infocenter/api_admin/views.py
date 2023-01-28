from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import DestroyAPIView, ListAPIView
from rest_framework.response import Response

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from common.paginations import StandardResultsSetPagination
from common.permissions import IsAdminOrSuperAdminOrDirector

from ..models import CourseInfo, CourseInfoCategory, WebResource
from .serializers import (
    CourseInfoCategoryCRUDSerializer,
    CourseInfoCategoryListSerializer,
    CourseInfoCRUDSerializer,
    CourseInfoListSerializer,
    WebResourceCRUDAdminSerializer,
)


class CourseInfoCategoryViewSet(viewsets.ModelViewSet):
    """CourseInfoCategory viewset."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = CourseInfoCategory.objects.all()
    serializer_class = CourseInfoCategoryCRUDSerializer

    def list(self, request, *args, **kwargs):
        """List all course info categories."""
        queryset = self.get_queryset()
        serializer = CourseInfoCategoryListSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseInfoViewSet(viewsets.ModelViewSet):
    """CourseInfo viewset."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = CourseInfo.objects.all()
    serializer_class = CourseInfoCRUDSerializer

    def list(self, request, *args, **kwargs):
        """List all course infos."""
        queryset = self.get_queryset()
        serializer = CourseInfoListSerializer(queryset, many=True)
        return Response(serializer.data)


class WebResourceCreateAPIView(BaseCreatorCreateAPIView):
    """WebResource viewset."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = WebResource.objects.all()
    serializer_class = WebResourceCRUDAdminSerializer


class WebResourceUpdateAPIView(BaseCreatorUpdateAPIView):
    """WebResource viewset."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = WebResource.objects.all()
    serializer_class = WebResourceCRUDAdminSerializer


class WebResourceListAPIView(ListAPIView):
    """WebResource viewset."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = WebResource.objects.all()
    serializer_class = WebResourceCRUDAdminSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title"]
    pagination_class = StandardResultsSetPagination


class WebResourceDeleteAPIView(DestroyAPIView):
    """WebResource viewset."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = WebResource.objects.all()
