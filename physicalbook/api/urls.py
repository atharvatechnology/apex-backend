from django.urls import path

from physicalbook.api.views import (
    PhysicalBookCreateAPIView,
    PhysicalBookDestroyAPIView,
    PhysicalBookListAPIView,
    PhysicalBookRetrieveAPIViewAfterEnroll,
    PhysicalBookRetrieveAPIViewBeforeEnroll,
    PhysicalBookUpdateAPIView,
)

urlpatterns = [
    path("list/", PhysicalBookListAPIView.as_view(), name="book-list"),
    path("create/", PhysicalBookCreateAPIView.as_view(), name="book-create"),
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
    path("update/<int:pk>/", PhysicalBookUpdateAPIView.as_view(), name="book-update"),
    path("delete/<int:pk>/", PhysicalBookDestroyAPIView.as_view(), name="book-delete"),
]
