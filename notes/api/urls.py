from django.urls import include, path

from notes.api.views import (
    ContentListAPIView,
    ContentRetrieveAPIViewAfterEnroll,
    ContentRetrieveAPIViewBeforeEnroll,
    NoteListAPIVew,
    NoteRetrieveAPIViewAfterEnroll,
    NoteRetrieveAPIViewBeforeEnroll,
    RecordedVideoListAPIView,
    RecordedVideoRetrieveAPIView,
)

app_name = "notes"

note_urls = [
    path("list/", NoteListAPIVew.as_view(), name="note-list"),
    path(
        "get/after/<int:pk>/",
        NoteRetrieveAPIViewAfterEnroll.as_view(),
        name="note-retrieve-after-enroll",
    ),
    path(
        "get/before/<int:pk>/",
        NoteRetrieveAPIViewBeforeEnroll.as_view(),
        name="note-retrieve-before-enroll",
    ),
]

content_urls = [
    path("content/list/", ContentListAPIView.as_view(), name="content-list"),
    path(
        "content/get/after/<int:pk>/",
        ContentRetrieveAPIViewAfterEnroll.as_view(),
        name="content-retrieve-after-enroll",
    ),
    path(
        "content/get/before/<int:pk>/",
        ContentRetrieveAPIViewBeforeEnroll.as_view(),
        name="content-retrieve-before-enroll",
    ),
]

recorded_video_urls = [
    path("list/", RecordedVideoListAPIView.as_view(), name="recorded-video-list"),
    path(
        "retrieve/<int:pk>/",
        RecordedVideoRetrieveAPIView.as_view(),
        name="recorded-video-retrieve",
    ),
]

urlpatterns = [
    path("", include(note_urls)),
    path("content/", include(content_urls)),
    path("recorded-video/", include(recorded_video_urls)),
]
