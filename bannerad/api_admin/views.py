from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from bannerad.api_admin.serializers import (
    BannerAdCreateAdminSerializer,
    BannerAdListAdminSerializer,
    BannerAdRetrieveAdminSerializer,
    BannerAdUpdateAdminSerializer,
)
from bannerad.models import BannerAd
from common.api.views import BaseCreatorCreateAPIView
from common.permissions import IsAdminOrSuperAdminOrDirector


class BannerAdCreateAdminAPIView(BaseCreatorCreateAPIView):
    """View for creating bannerad."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    serializer_class = BannerAdCreateAdminSerializer
    queryset = BannerAd.objects.all()


class BannerAdRetrieveAdminAPIView(RetrieveAPIView):
    """View for retrieving bannerad."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    serializer_class = BannerAdRetrieveAdminSerializer
    queryset = BannerAd.objects.all()


class BannerAdListAdminAPIView(ListAPIView):
    """View for listing bannerad."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    serializer_class = BannerAdListAdminSerializer
    queryset = BannerAd.objects.all()


class BannerAdUpdateAdminAPIView(UpdateAPIView):
    """View for updating bannerad."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    serializer_class = BannerAdUpdateAdminSerializer
    queryset = BannerAd.objects.all()


class BannerAdDeleteAdminAPIView(DestroyAPIView):
    """View for deleting bannerad."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = BannerAd.objects.all()
