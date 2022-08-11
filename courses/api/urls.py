from django.urls import path

from courses.api.views import (
    CourseCategoryListAPIView,
    CourseCategoryRetrieveAPIView,
    CourseListAPIView,
    CourseRetrieveAPIViewBeforeEnroll,
)

urlpatterns = [
    path("list/", CourseListAPIView.as_view(), name="course-list"),
    # path(
    #     "retrieve/<int:pk>/",
    #     CourseRetrieveAPIViewAfterEnroll.as_view(),
    #     name="course-retrieve-after-enroll",
    # ),
    path(
        "retrieve/<int:pk>/",
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
