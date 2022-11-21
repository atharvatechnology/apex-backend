from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from bannerad.api.serializers import BannerAdRetrieveSerializer
from bannerad.models import BannerAd


class BannerAdRetrieveAPIView(RetrieveAPIView):
    """View for creating bannerad."""

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = BannerAdRetrieveSerializer
    queryset = BannerAd.objects.all()
