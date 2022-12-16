from django.urls import include, path

from .views import (
    CourseCategoryCreateAPIView,
    CourseCategoryDeleteAPIView,
    CourseCategoryListAPIView,
    CourseCategoryRetrieveAPIView,
    CourseCategoryUpdateAPIView,
    CourseCreateAPIView,
    CourseDeleteAPIView,
    CourseDropdownListAPIView,
    CourseListAPIView,
    CourseOverviewAPIView,
    CourseOverviewCardAPIView,
    CourseRetrieveAPIView,
    CourseUpdateAPIView,
    remove_exam_in_course,
)

course_overview_urlpatterns = [
    path("", CourseOverviewAPIView.as_view(), name="course-overview"),
    path("card/", CourseOverviewCardAPIView.as_view(), name="course-overview-card"),
]

course_urlpatterns = [
    path("create/", CourseCreateAPIView.as_view(), name="course-create"),
    path("list/", CourseListAPIView.as_view(), name="course-list"),
    path("retrieve/<int:pk>/", CourseRetrieveAPIView.as_view(), name="course-get"),
    path("delete/<int:pk>/", CourseDeleteAPIView.as_view(), name="course-delete"),
    path("update/<int:pk>/", CourseUpdateAPIView.as_view(), name="course-update"),
    path(
        "list/dropdown/",
        CourseDropdownListAPIView.as_view(),
        name="course-list-dropdown",
    ),
    path("exam/remove/", remove_exam_in_course, name="remove-exam-in-course"),
    path("overview/", include(course_overview_urlpatterns)),
]

category_urlpatterns = [
    path("create/", CourseCategoryCreateAPIView.as_view(), name="category-create"),
    path("list/", CourseCategoryListAPIView.as_view(), name="category-list"),
    path(
        "retrieve/<int:pk>/",
        CourseCategoryRetrieveAPIView.as_view(),
        name="category-get",
    ),
    path(
        "update/<int:pk>/",
        CourseCategoryUpdateAPIView.as_view(),
        name="category-update",
    ),
    path(
        "delete/<int:pk>/",
        CourseCategoryDeleteAPIView.as_view(),
        name="category-delete",
    ),
]

urlpatterns = [
    path("", include(course_urlpatterns)),
    path("category/", include(category_urlpatterns)),
]
