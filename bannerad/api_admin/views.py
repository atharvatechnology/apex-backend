from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from bannerad.api_admin.serializers import (
    BannerAdCreateSerializer,
    BannerAdDeleteSerializer,
    BannerAdListSerializer,
    BannerAdRetrieveSerializer,
    BannerAdUpdateSerializer,
)
from bannerad.models import BannerAd
from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView


class BannerAdCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdCreateSerializer
    queryset = BannerAd.objects.all()


class BannerAdListAPIView(ListAPIView):
    """View for listing bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    queryset = BannerAd.objects.all()


class BannerAdRetrieveAPIView(RetrieveAPIView):
    """View for retrieving bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdRetrieveSerializer
    queryset = BannerAd.objects.all()


class BannerAdUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdUpdateSerializer
    queryset = BannerAd.objects.all()


class BannerAdDeleteAPIView(DestroyAPIView):
    """View for deleting bannerad."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BannerAdDeleteSerializer
    queryset = BannerAd.objects.all()
