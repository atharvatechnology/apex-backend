from django.urls import path

from physicalbook.api.views import (
    PhysicalBookListAPIView,
    PhysicalBookRetrieveAPIViewAfterEnroll,
    PhysicalBookRetrieveAPIViewBeforeEnroll,
)

urlpatterns = [
    path("list/", PhysicalBookListAPIView.as_view(), name="book-list"),
    path(
        "get/after/<int:pk>/",
        PhysicalBookRetrieveAPIViewAfterEnroll.as_view(),
        name="book-retieve-after-enroll",
    ),
    path(
        "get/before/<int:pk>/",
        PhysicalBookRetrieveAPIViewBeforeEnroll.as_view(),
        name="book-retrieve-before-enroll",
    ),
]
