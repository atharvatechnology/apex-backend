from django.urls import path

from bannerad.api_admin.views import BannerAdCreateAPIView

urlpatterns = [
    path("create/", BannerAdCreateAPIView.as_view(), name="bannerad-create"),
]
