from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from bannerad.api_admin.serializers import (
    BannerAdCreateSerializer,
    BannerAdListSerializer,
    BannerAdRetrieveSerializer,
    BannerAdUpdateSerializer,
)
from bannerad.models import BannerAd
from common.api.views import BaseCreatorCreateAPIView


class BannerAdCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdCreateSerializer
    queryset = BannerAd.objects.all()


class BannerAdRetrieveAPIView(RetrieveAPIView):
    """View for retrieving bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdRetrieveSerializer
    queryset = BannerAd.objects.all()


class BannerAdListAPIView(ListAPIView):
    """View for listing bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdListSerializer
    queryset = BannerAd.objects.all()


class BannerAdUpdateAPIView(UpdateAPIView):
    """View for updating bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdUpdateSerializer
    queryset = BannerAd.objects.all()


class BannerAdDeleteAPIView(DestroyAPIView):
    """View for deleting bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = BannerAd.objects.all()
