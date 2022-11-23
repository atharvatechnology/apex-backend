from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from common.paginations import StandardResultsSetPagination
from counseling.api_admin.serializers import (
    CounselingCreateSerializer,
    CounselingListSerializer,
    CounselingRetrieveSerializer,
    CounselingUpdateSerializer,
)
from counseling.filters import CounselingFilter
from counseling.models import Counseling


class CounselingListAPIView(ListAPIView):
    """View for listing counseling."""

    permission_classes = [AllowAny]
    serializer_class = CounselingListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["student_name", "phone_number"]
    filterset_class = CounselingFilter
    pagination_class = StandardResultsSetPagination
    queryset = Counseling.objects.all()


class CounselingCreateAPIView(CreateAPIView):
    """View for creating counseling."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CounselingCreateSerializer
    queryset = Counseling.objects.all()

    def perform_create(self, serializer):
        return serializer.save(counsellor=self.request.user)


class CounselingRetrieveAPIView(RetrieveAPIView):
    """View for retrieving counseling."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CounselingRetrieveSerializer
    queryset = Counseling.objects.all()


class CounselingUpdateAPIView(UpdateAPIView):
    """View for updating counseling."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CounselingUpdateSerializer
    queryset = Counseling.objects.all()
