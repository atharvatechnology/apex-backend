from django.urls import path

from counseling.api_admin.views import (
    CounselingCreateAPIView,
    CounselingDeleteAPIView,
    CounselingListAPIView,
    CounselingRetrieveAPIView,
    CounselingUpdateAPIView,
)

urlpatterns = [
    path("create/", CounselingCreateAPIView.as_view(), name="counseling-create"),
    path("list/", CounselingListAPIView.as_view(), name="counseling-list"),
    path(
        "retrieve/<int:pk>/",
        CounselingRetrieveAPIView.as_view(),
        name="counseling-retrieve",
    ),
    path(
        "update/<int:pk>/", CounselingUpdateAPIView.as_view(), name="counseling-delete"
    ),
    path(
        "delete/<int:pk>/", CounselingDeleteAPIView.as_view(), name="counseling-delete"
    ),
]
