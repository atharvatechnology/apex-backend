from django.urls import path

from bannerad.api_admin.views import (
    BannerAdCreateAPIView,
    BannerAdDeleteAPIView,
    BannerAdListAPIView,
    BannerAdRetrieveAPIView,
    BannerAdUpdateAPIView,
)

urlpatterns = [
    path("create/", BannerAdCreateAPIView.as_view(), name="bannerad-create"),
    path("list/", BannerAdListAPIView.as_view(), name="bannerad-create"),
    path(
        "retrieve/<int:pk>/",
        BannerAdRetrieveAPIView.as_view(),
        name="bannerad-retrieve",
    ),
    path(
        "update/<int:pk>/",
        BannerAdUpdateAPIView.as_view(),
        name="bannerad-update",
    ),
    path(
        "delete/<int:pk>/",
        BannerAdDeleteAPIView.as_view(),
        name="bannerad-delete",
    ),
]
