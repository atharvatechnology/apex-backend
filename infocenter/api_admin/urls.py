from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CourseInfoCategoryViewSet,
    CourseInfoViewSet,
    WebResourceCreateAPIView,
    WebResourceDeleteAPIView,
    WebResourceListAPIView,
    WebResourceUpdateAPIView,
)

router = DefaultRouter()

router.register(
    r"course-info-category", CourseInfoCategoryViewSet, basename="course-info-category"
)
router.register(r"course-info", CourseInfoViewSet, basename="course-info")

webresource_urls = [
    path("create/", WebResourceCreateAPIView.as_view(), name="WebResource-create"),
    path(
        "update/<int:pk>/",
        WebResourceUpdateAPIView.as_view(),
        name="WebResource-update",
    ),
    path("list/", WebResourceListAPIView.as_view(), name="WebResource-list"),
    path(
        "delete/<int:pk>/",
        WebResourceDeleteAPIView.as_view(),
        name="WebResource-delete",
    ),
]

urlpatterns = [
    path("", include(router.urls)),
    path("web-resource/", include(webresource_urls)),
]
