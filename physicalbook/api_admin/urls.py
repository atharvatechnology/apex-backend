from django.urls import path

from physicalbook.api_admin.views import (
    PhysicalBookAdminCreateAPIView,
    PhysicalBookAdminDeleteAPIView,
    PhysicalBookAdminListAPIView,
    PhysicalBookAdminRetrieveAPIView,
    PhysicalBookAdminUpdateAPIView,
    PhysicalBookCourseAdminListAPIView,
)

urlpatterns = [
    path("create/", PhysicalBookAdminCreateAPIView.as_view(), name="admin-book-create"),
    path("list/", PhysicalBookAdminListAPIView.as_view(), name="admin-book-list"),
    path(
        "list/<int:course_id>/",
        PhysicalBookCourseAdminListAPIView.as_view(),
        name="admin-book-list-course",
    ),
    path(
        "retrieve/<int:pk>/",
        PhysicalBookAdminRetrieveAPIView.as_view(),
        name="admin-book-retrieve",
    ),
    path(
        "update/<int:pk>/",
        PhysicalBookAdminUpdateAPIView.as_view(),
        name="admin-book-update",
    ),
    path(
        "delete/<int:pk>/",
        PhysicalBookAdminDeleteAPIView.as_view(),
        name="admin-book-delete",
    ),
]
