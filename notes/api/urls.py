from django.urls import path

from notes.api.views import (
    ContentCreateAPIView,
    ContentDestroyAPIView,
    ContentListAPIView,
    ContentUpdateAPIView,
    NoteCreateAPIView,
    NoteDestroyAPIView,
    NoteListAPIVew,
    NoteUpdateAPIView,
)

app_name = "notes"

urlpatterns = [
    path("list/", NoteListAPIVew.as_view(), name="note-list"),
    path("create/", NoteCreateAPIView.as_view(), name="note-create"),
    path("update/<int:pk>/", NoteUpdateAPIView.as_view(), name="note-update"),
    path("delete/<int:pk>/", NoteDestroyAPIView.as_view(), name="note-delete"),
    path("content/list/", ContentListAPIView.as_view(), name="content-list"),
    path("content/create/", ContentCreateAPIView.as_view(), name="content-create"),
    path(
        "content/update/<int:pk>/",
        ContentUpdateAPIView.as_view(),
        name="content-update",
    ),
    path(
        "content/delete/<int:pk>/",
        ContentDestroyAPIView.as_view(),
        name="content-delete",
    ),
]
