from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from bannerads.api_admin.serializers import BannerAdCreateSerializer
from bannerads.models import BannerAd


class BannerAdCreateAPIView(CreateAPIView):
    """View for creating bannerad."""

    permission_classes = [IsAuthenticated]
    serializer_class = BannerAdCreateSerializer
    queryset = BannerAd.objects.all()
