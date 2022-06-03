from django.urls import path

from courses.api.views import (
    CourseCategoryCreateAPIView,
    CourseCategoryDeleteAPIView,
    CourseCategoryListAPIView,
    CourseCategoryRetrieveAPIView,
    CourseCategoryUpdateAPIView,
    CourseCreateAPIView,
    CourseDeleteAPIView,
    CourseListAPIView,
    CourseRetrieveAPIView,
    CourseUpdateAPIView,
)

urlpatterns = [
    path("list/", CourseListAPIView.as_view(), name="course-list"),
    path("create/", CourseCreateAPIView.as_view(), name="course-create"),
    path("get/<int:pk>/", CourseRetrieveAPIView.as_view(), name="course-retrieve"),
    path("update/<int:pk>/", CourseUpdateAPIView.as_view(), name="course-update"),
    path("delete/<int:pk>/", CourseDeleteAPIView.as_view(), name="course-delete"),
    path("categories/list", CourseCategoryListAPIView.as_view(), name="category-list"),
    path(
        "categories/create/",
        CourseCategoryCreateAPIView.as_view(),
        name="category-create",
    ),
    path(
        "categories/<int:pk>",
        CourseCategoryRetrieveAPIView.as_view(),
        name="category-retrieve",
    ),
    path(
        "categories/update/<int:pk>/",
        CourseCategoryUpdateAPIView.as_view(),
        name="category-update",
    ),
    path(
        "categories/delete/<int:pk>/",
        CourseCategoryDeleteAPIView.as_view(),
        name="category-delete",
    ),
]
