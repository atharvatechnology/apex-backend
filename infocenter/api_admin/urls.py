from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseInfoCategoryViewSet, CourseInfoViewSet

router = DefaultRouter()

router.register(
    r"course-info-category", CourseInfoCategoryViewSet, basename="course-info-category"
)
router.register(r"course-info", CourseInfoViewSet, basename="course-info")

urlpatterns = [
    path("", include(router.urls)),
]
