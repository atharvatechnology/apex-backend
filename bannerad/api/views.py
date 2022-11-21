from rest_framework.permissions import IsAuthenticated

from bannerad.api.serializers import BannerAdRetrieveSerializer
from bannerad.models import BannerAd
from common.api.views import BaseCreatorCreateAPIView


class BannerAdRetrieveAPIView(BaseCreatorCreateAPIView):
    """View for creating bannerad."""

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = BannerAdRetrieveSerializer
    queryset = BannerAd.objects.all()
