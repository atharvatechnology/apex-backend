from django.urls import path

from courses.api.views import (
    CourseCategoryListAPIView,
    CourseCategoryRetrieveAPIView,
    CourseListAPIView,
    CourseRetrieveAPIViewAfterEnroll,
    CourseRetrieveAPIViewBeforeEnroll,
)

urlpatterns = [
    path("list/", CourseListAPIView.as_view(), name="course-list"),
    path(
        "get/after/<int:pk>/",
        CourseRetrieveAPIViewAfterEnroll.as_view(),
        name="course-retrieve-after-enroll",
    ),
    path(
        "get/before/<int:pk>/",
        CourseRetrieveAPIViewBeforeEnroll.as_view(),
        name="course-retrieve-before-enroll",
    ),
    path("categories/list", CourseCategoryListAPIView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>",
        CourseCategoryRetrieveAPIView.as_view(),
        name="category-retrieve",
    ),
]
