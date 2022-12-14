from rest_framework.filters import SearchFilter
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from physicalbook.api_admin.serializers import (
    PhysicalBookAdminCreateSerializer,
    PhysicalBookAdminListSerializer,
    PhysicalBookAdminRetrieveSerializer,
    PhysicalBookAdminUpdateSerializer,
)
from physicalbook.models import PhysicalBook


class PhysicalBookAdminCreateAPIView(BaseCreatorCreateAPIView):
    """Views for creating physicalbook for admin."""

    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = PhysicalBook.objects.all()
    serializer_class = PhysicalBookAdminCreateSerializer


class PhysicalBookAdminListAPIView(ListAPIView):
    """Views for listing PhysicalBook."""

    serializer_class = PhysicalBookAdminListSerializer
    search_fields = ["name"]
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [SearchFilter]
    queryset = PhysicalBook.objects.all()


class PhysicalBookAdminRetrieveAPIView(RetrieveAPIView):
    """Views for retrieving physicalbook for admin."""

    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = PhysicalBook.objects.all()
    serializer_class = PhysicalBookAdminRetrieveSerializer


class PhysicalBookAdminUpdateAPIView(BaseCreatorUpdateAPIView):
    """Views for updating physicalbook for admin."""

    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = PhysicalBook.objects.all()
    serializer_class = PhysicalBookAdminUpdateSerializer


class PhysicalBookAdminDeleteAPIView(DestroyAPIView):
    """Views for deleting physicalbook for admin."""

    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = PhysicalBook.objects.all()
