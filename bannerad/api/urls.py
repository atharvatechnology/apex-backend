from django.urls import path

from .views import BannerAdRetrieveAPIView

urlpatterns = [
    path(
        "retrieve/<int:pk>/",
        BannerAdRetrieveAPIView.as_view(),
        name="bannerad-retrieve",
    ),
]
