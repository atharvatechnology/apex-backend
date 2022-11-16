from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from counseling.api.serializers import (
    CounselingDeleteSerializer,
    CounselingListSerializer,
    CounselingRetrieveSerializer,
    CounselingUpdateSerializer,
)
from counseling.models import Counseling


class CounselingListAPIView(ListAPIView):
    """View for listing counseling."""

    permission_classes = [AllowAny]
    serializer_class = CounselingListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["student_name", "phone_number"]
    queryset = Counseling.objects.all()


class CounselingRetrieveAPIView(RetrieveAPIView):
    """View for retrieving counseling."""

    permission_classes = [IsAuthenticated]
    serializer_class = CounselingRetrieveSerializer
    queryset = Counseling.objects.all()


class CounselingUpdateAPIView(UpdateAPIView):
    """View for updating counseling."""

    permission_classes = [IsAuthenticated]
    serializer_class = CounselingUpdateSerializer
    queryset = Counseling.objects.all()


class CounselingDeleteAPIView(DestroyAPIView):
    """View for deleting counseling."""

    permission_classes = [IsAuthenticated]
    serializer_class = CounselingDeleteSerializer
    queryset = Counseling.objects.all()
