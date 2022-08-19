from django.urls import path

from courses.api.views import (
    CourseCategoryListAPIView,
    CourseCategoryRetrieveAPIView,
    CourseListAPIView,
    CourseRetrieveAPIAfterEnrollView,
    CourseRetrieveAPIBeforeEnrollView,
)

urlpatterns = [
    path("list/", CourseListAPIView.as_view(), name="course-list"),
    path(
        "retrieve/before-enroll/<int:pk>/",
        CourseRetrieveAPIBeforeEnrollView.as_view(),
        name="course-retrieve-before-enroll",
    ),
    path(
        "retrieve/after-enroll/<int:pk>/",
        CourseRetrieveAPIAfterEnrollView.as_view(),
        name="course-retrieve-after-enroll",
    ),
    path("categories/list", CourseCategoryListAPIView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>",
        CourseCategoryRetrieveAPIView.as_view(),
        name="category-retrieve",
    ),
]
