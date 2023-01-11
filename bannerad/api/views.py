from django.shortcuts import get_list_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from bannerad.api.serializers import BannerAdRetrieveSerializer
from bannerad.models import BannerAd, BannerAdCategory


class BannerAdRetrieveAPIView(RetrieveAPIView):
    """View for creating bannerad."""

    permission_classes = [AllowAny]
    serializer_class = BannerAdRetrieveSerializer
    queryset = BannerAd.objects.all()


class BannerAdGetWebAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BannerAdRetrieveSerializer
    queryset = BannerAd.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_list_or_404(
            queryset, is_displayed=True, category=BannerAdCategory.WEB
        )
        return obj[0]


class BannerAdGetMobileAPIView(BannerAdGetWebAPIView):
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_list_or_404(
            queryset, is_displayed=True, category=BannerAdCategory.MOBILE
        )
        return obj[0]
