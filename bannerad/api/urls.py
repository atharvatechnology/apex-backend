from django.urls import path

from .views import (
    BannerAdGetMobileAPIView,
    BannerAdGetWebAPIView,
    BannerAdRetrieveAPIView,
)

app_name = "bannerad.api"

urlpatterns = [
    path(
        "retrieve/<int:pk>/",
        BannerAdRetrieveAPIView.as_view(),
        name="retrieve",
    ),
    path("get/web/", BannerAdGetWebAPIView.as_view(), name="get-web"),
    path("get/mobile/", BannerAdGetMobileAPIView.as_view(), name="get-mobile"),
]
