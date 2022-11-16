from django.urls import path

from counseling.api.views import CounselingListAPIView

urlpatterns = [
    path("list/", CounselingListAPIView.as_view(), name="counseling-list"),
]
