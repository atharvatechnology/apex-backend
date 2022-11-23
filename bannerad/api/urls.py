from django.urls import path

from bannerad.api_admin.views import BannerAdRetrieveAPIView

urlpatterns = [
    path(
        "retrieve/<int:pk>/",
        BannerAdRetrieveAPIView.as_view(),
        name="bannerad-retrieve",
    ),
]
