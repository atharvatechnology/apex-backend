from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from common.paginations import StandardResultsSetPagination

from ..models import CourseInfo, CourseInfoCategory, WebResouce
from .serializers import (
    CourseInfoCategoryCRUDSerializer,
    CourseInfoCategoryListSerializer,
    CourseInfoCRUDSerializer,
    CourseInfoListSerializer,
    WebResouceCRUDAdminSerializer,
)


class CourseInfoCategoryViewSet(viewsets.ModelViewSet):
    """CourseInfoCategory viewset."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CourseInfoCategory.objects.all()
    serializer_class = CourseInfoCategoryCRUDSerializer

    def list(self, request, *args, **kwargs):
        """List all course info categories."""
        queryset = self.get_queryset()
        serializer = CourseInfoCategoryListSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseInfoViewSet(viewsets.ModelViewSet):
    """CourseInfo viewset."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CourseInfo.objects.all()
    serializer_class = CourseInfoCRUDSerializer

    def list(self, request, *args, **kwargs):
        """List all course infos."""
        queryset = self.get_queryset()
        serializer = CourseInfoListSerializer(queryset, many=True)
        return Response(serializer.data)


class WebResouceCreateAPIView(BaseCreatorCreateAPIView):
    """WebResouce viewset."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = WebResouce.objects.all()
    serializer_class = WebResouceCRUDAdminSerializer


class WebResouceUpdateAPIView(BaseCreatorUpdateAPIView):
    """WebResouce viewset."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = WebResouce.objects.all()
    serializer_class = WebResouceCRUDAdminSerializer


class WebResouceListAPIView(ListAPIView):
    """WebResouce viewset."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = WebResouce.objects.all()
    serializer_class = WebResouceCRUDAdminSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title"]
    pagination_class = StandardResultsSetPagination


class WebResouceDeleteAPIView(DestroyAPIView):
    """WebResouce viewset."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = WebResouce.objects.all()
