from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CourseInfoCategoryViewSet,
    CourseInfoViewSet,
    WebResouceCreateAPIView,
    WebResouceDeleteAPIView,
    WebResouceListAPIView,
    WebResouceUpdateAPIView,
)

router = DefaultRouter()

router.register(
    r"course-info-category", CourseInfoCategoryViewSet, basename="course-info-category"
)
router.register(r"course-info", CourseInfoViewSet, basename="course-info")

WebResouce_urls = [
    path("create/", WebResouceCreateAPIView.as_view(), name="WebResouce-create"),
    path(
        "update/<int:pk>/", WebResouceUpdateAPIView.as_view(), name="WebResouce-update"
    ),
    path("list/", WebResouceListAPIView.as_view(), name="WebResouce-list"),
    path(
        "delete/<int:pk>/", WebResouceDeleteAPIView.as_view(), name="WebResouce-delete"
    ),
]

urlpatterns = [
    path("", include(router.urls)),
    # path("WebResouce/", include(WebResouce_urls)),
]
