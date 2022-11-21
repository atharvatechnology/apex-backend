from rest_framework.permissions import IsAdminUser, IsAuthenticated

from bannerad.api_admin.serializers import BannerAdCreateSerializer
from bannerad.models import BannerAd
from common.api.views import BaseCreatorCreateAPIView


class BannerAdCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdCreateSerializer
    queryset = BannerAd.objects.all()
