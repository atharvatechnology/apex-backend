from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from counseling.api.serializers import CounselingSerializer
from counseling.models import Counseling


class CounselingListAPIView(ListAPIView):
    """View for listing counseling."""

    permission_classes = [AllowAny]
    serializer_class = CounselingSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["student_name", "phone_number"]
    queryset = Counseling.objects.all()
