from django.urls import include, path

from .views import (
    CourseInfoCategoryListAPIView,
    CourseInfoCategoryRetrieveAPIView,
    CourseInfoListAPIView,
    CourseInfoRetrieveAPIView,
)

course_info_category_urlpatterns = [
    path(
        "list/",
        CourseInfoCategoryListAPIView.as_view(),
        name="course-info-category-list",
    ),
    path(
        "retrieve/<int:pk>/",
        CourseInfoCategoryRetrieveAPIView.as_view(),
        name="course-info-category-retrieve",
    ),
]

course_info_urlpatterns = [
    path("list/", CourseInfoListAPIView.as_view(), name="course-info-list"),
    path(
        "retrieve/<int:pk>/",
        CourseInfoRetrieveAPIView.as_view(),
        name="course-info-retrieve",
    ),
]

urlpatterns = [
    path("course-info-category/", include(course_info_category_urlpatterns)),
    path("course-info/", include(course_info_urlpatterns)),
]
