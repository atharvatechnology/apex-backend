from django.urls import path

from bannerad.api_admin.views import (
    BannerAdCreateAdminAPIView,
    BannerAdDeleteAdminAPIView,
    BannerAdListAdminAPIView,
    BannerAdRetrieveAdminAPIView,
    BannerAdUpdateAdminAPIView,
)

# app_name = 'bannerad.api.admin'

urlpatterns = [
    path("create/", BannerAdCreateAdminAPIView.as_view(), name="bannerad-create"),
    path("list/", BannerAdListAdminAPIView.as_view(), name="bannerad-list"),
    path(
        "retrieve/<int:pk>/",
        BannerAdRetrieveAdminAPIView.as_view(),
        name="bannerad-retrieve",
    ),
    path(
        "update/<int:pk>/",
        BannerAdUpdateAdminAPIView.as_view(),
        name="bannerad-update",
    ),
    path(
        "delete/<int:pk>/",
        BannerAdDeleteAdminAPIView.as_view(),
        name="bannerad-delete",
    ),
]
