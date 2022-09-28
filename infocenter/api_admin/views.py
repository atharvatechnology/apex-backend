from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from ..models import CourseInfo, CourseInfoCategory
from .serializers import (
    CourseInfoCategoryCRUDSerializer,
    CourseInfoCategoryListSerializer,
    CourseInfoCRUDSerializer,
    CourseInfoListSerializer,
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
