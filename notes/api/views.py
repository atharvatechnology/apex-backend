from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from courses.api.permissions import IsCourseEnrolledActive
from notes.api.serializers import (
    ContentSerializerAfterEnroll,
    ContentSerializerBeforeEnroll,
    NoteSerializerAfterEnroll,
    NoteSerializerBeforeEnroll,
    RecordedVideoDetailSerializer,
    RecordedVideoListSerializer,
)
from notes.models import Content, Note, RecordedVideo


# Start Note API
class NoteListAPIVew(ListAPIView):
    """permits to list data of notes.

    Parameters
    ----------
    ListAPIView : cls
        The view provides read-only endpoints
        to represent a collection of model instances

    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializerBeforeEnroll
    filter_backends = [SearchFilter]
    search_fields = ["title"]


class NoteRetrieveAPIViewAfterEnroll(RetrieveAPIView):
    """Allows every detail data of notes to enrolled user.

    Parameters
    ----------
    RetrieveAPIView : cls

        The view allows to view a single
        data of particular list view after
        the user get enrolled

    """

    permission_classes = [IsCourseEnrolledActive]
    queryset = Note.objects.all()
    serializer_class = NoteSerializerAfterEnroll


class NoteRetrieveAPIViewBeforeEnroll(RetrieveAPIView):
    """Allows only unrestricted detail data of notes to  unenrolled user.

    Parameters
    ----------
    RetrieveAPIView : cls
        The view allows to view a single
        data of particular list view without
        the user getting enrolled

    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializerBeforeEnroll


# End Note API


# Start Content API
class ContentListAPIView(ListAPIView):
    """permits list of data of content.

    Parameters
    ----------
    ListAPIView : cls
        The view provides read-only
        endpoints to represent a collection
        of model instances

    """

    queryset = Content.objects.all()
    serializer_class = ContentSerializerBeforeEnroll
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["type"]


class ContentRetrieveAPIViewBeforeEnroll(RetrieveAPIView):
    """permits unrestricted detail data of content to unenrolled user.

    Parameters
    ----------
    RetrieveAPIView : cls
        The view allows to view a single
        data of particular list view
        without the user getting enrolled

    """

    permission_classes = [IsCourseEnrolledActive]
    queryset = Content.objects.all()
    serializer_class = ContentSerializerBeforeEnroll


class ContentRetrieveAPIViewAfterEnroll(RetrieveAPIView):
    """permits detail data of content after the user get enrolled.

    Parameters
    ----------
    RetrieveAPIView : cls
        The view allows to view a single
        data of particular list view after
        the user get enrolled

    """

    permission_classes = [IsCourseEnrolledActive]
    queryset = Content.objects.all()
    serializer_class = ContentSerializerAfterEnroll


class RecordedVideoListAPIView(ListAPIView):
    permission_classes = [IsCourseEnrolledActive]
    serializer_class = RecordedVideoListSerializer
    queryset = RecordedVideo.objects.all()


class RecordedVideoRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsCourseEnrolledActive]
    serializer_class = RecordedVideoDetailSerializer
    queryset = RecordedVideo.objects.all()
