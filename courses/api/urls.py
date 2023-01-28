from django.urls import include, path

from courses.api.views import (
    CourseCategoryListAPIView,
    CourseCategoryRetrieveAPIView,
    CourseListAPIView,
    CourseRetrieveAPIAfterEnrollView,
    CourseRetrieveAPIBeforeEnrollView,
)
from enrollments.api.views import CourseExamEnrollmentCreateAPIView

app_name = "api.courses"

course_exam_urls = [
    path(
        "<int:exam_id>/enroll/",
        CourseExamEnrollmentCreateAPIView.as_view(),
        name="exam-enroll",
    ),
]

categories_url = [
    path("list", CourseCategoryListAPIView.as_view(), name="category-list"),
    path(
        "<int:pk>",
        CourseCategoryRetrieveAPIView.as_view(),
        name="category-retrieve",
    ),
]

courses_url = [
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
    path("<int:pk>/exam/", include(course_exam_urls)),
]


urlpatterns = [
    path("", include(courses_url)),
    path("categories/", include(categories_url)),
]
