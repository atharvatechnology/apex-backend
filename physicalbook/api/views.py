from rest_framework.filters import SearchFilter
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from physicalbook.api.serializers import (
    PhysicalBookCreateSerializer,
    PhysicalBookSerializerAfterEnroll,
    PhysicalBookSerializerBeforeEnroll,
)
from physicalbook.models import PhysicalBook

# Start Physical book api


class PhysicalBookListAPIView(ListAPIView):
    """ListAPIView provides end point to shows model instances."""

    queryset = PhysicalBook.objects.all()
    serializer_class = PhysicalBookSerializerBeforeEnroll
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class PhysicalBookRetrieveAPIViewBeforeEnroll(RetrieveAPIView):
    """Provides single data of particular view to unenrolled user."""

    queryset = PhysicalBook.objects.all()
    serializer_class = PhysicalBookSerializerBeforeEnroll


class PhysicalBookRetrieveAPIViewAfterEnroll(RetrieveAPIView):
    """Provides single data of particular view to enrolled user."""

    queryset = PhysicalBook.objects.all()
    serializer_class = PhysicalBookSerializerAfterEnroll


class PhysicalBookCreateAPIView(BaseCreatorCreateAPIView):
    """Provides create only endpoint to the user."""

    queryset = PhysicalBook.objects.all()
    serializer_class = PhysicalBookCreateSerializer


class PhysicalBookUpdateAPIView(BaseCreatorUpdateAPIView):
    """Provides to update only endpoint for single model instance."""

    queryset = PhysicalBook.objects.all()
    serializer_class = PhysicalBookCreateSerializer


class PhysicalBookDestroyAPIView(DestroyAPIView):
    """provides destroy endpoint to single instance of pbook."""

    queryset = PhysicalBook.objects.all()
    serializer_class = PhysicalBookCreateSerializer
    permission_classes = [IsAuthenticated]


# End Physical book API
