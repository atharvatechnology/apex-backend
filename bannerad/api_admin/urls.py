from django.urls import path

from bannerad.api_admin.views import (
    BannerAdCreateAdminAPIView,
    BannerAdDeleteAdminAPIView,
    BannerAdListMobileAdminAPIView,
    BannerAdListWebAdminAPIView,
    BannerAdRetrieveAdminAPIView,
    BannerAdUpdateAdminAPIView,
)

app_name = "bannerad.api.admin"

urlpatterns = [
    path("create/", BannerAdCreateAdminAPIView.as_view(), name="create"),
    path("list/web/", BannerAdListWebAdminAPIView.as_view(), name="list-web"),
    path("list/mobile/", BannerAdListMobileAdminAPIView.as_view(), name="list-mobile"),
    path(
        "retrieve/<int:pk>/",
        BannerAdRetrieveAdminAPIView.as_view(),
        name="retrieve",
    ),
    path(
        "update/<int:pk>/",
        BannerAdUpdateAdminAPIView.as_view(),
        name="update",
    ),
    path(
        "delete/<int:pk>/",
        BannerAdDeleteAdminAPIView.as_view(),
        name="delete",
    ),
]
