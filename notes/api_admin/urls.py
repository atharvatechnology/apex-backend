from django.urls import include, path

from .views import (
    ContentCreateAPIView,
    ContentDestroyAPIView,
    ContentListAPIView,
    ContentListByCourseAPIView,
    ContentRetrieveAPIView,
    ContentUpdateAPIView,
    NoteCreateAPIView,
    NoteDestroyAPIView,
    NoteListAPIView,
    NoteRetrieveAPIView,
    NoteUpdateAPIView,
    RecordedVideoCreateAPIView,
    RecordedVideoDestroyAPIView,
    RecordedVideoListAPIView,
    RecordedVideoRetrieveAPIView,
    RecordedVideoUpdateAPIView,
)

note_urls = [
    path("list/<int:course_id>/", NoteListAPIView.as_view(), name="note-list"),
    path("create/", NoteCreateAPIView.as_view(), name="note-create"),
    path("retrieve/<int:pk>/", NoteRetrieveAPIView.as_view(), name="note-retrieve"),
    path("update/<int:pk>/", NoteUpdateAPIView.as_view(), name="note-update"),
    path("delete/<int:pk>/", NoteDestroyAPIView.as_view(), name="note-delete"),
]

content_urls = [
    path("list/", ContentListAPIView.as_view(), name="content-list"),
    path(
        "list/<int:course_id>/",
        ContentListByCourseAPIView.as_view(),
        name="content-course-list",
    ),
    path("create/", ContentCreateAPIView.as_view(), name="content-create"),
    path(
        "retrieve/<int:pk>/", ContentRetrieveAPIView.as_view(), name="content-retrieve"
    ),
    path("update/<int:pk>/", ContentUpdateAPIView.as_view(), name="content-update"),
    path("delete/<int:pk>/", ContentDestroyAPIView.as_view(), name="content-delete"),
]

recorded_video_urls = [
    path(
        "list/<int:course_id>/",
        RecordedVideoListAPIView.as_view(),
        name="recorded-video-list",
    ),
    path("create/", RecordedVideoCreateAPIView.as_view(), name="recorded-video-create"),
    path(
        "retrieve/<int:pk>/",
        RecordedVideoRetrieveAPIView.as_view(),
        name="recorded-video-retrieve",
    ),
    path(
        "update/<int:pk>/",
        RecordedVideoUpdateAPIView.as_view(),
        name="recorded-video-update",
    ),
    path(
        "delete/<int:pk>/",
        RecordedVideoDestroyAPIView.as_view(),
        name="recorded-video-delete",
    ),
]

urlpatterns = [
    path("", include(note_urls)),
    path("content/", include(content_urls)),
    path("recorded-video/", include(recorded_video_urls)),
]
