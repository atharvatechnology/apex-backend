from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from notes.api.serializers import (
    ContentCreateSerializer,
    ContentSerializerAfterEnroll,
    ContentSerializerBeforeEnroll,
    NoteCreateSerializer,
    NoteSerializerAfterEnroll,
    NoteSerializerBeforeEnroll,
)
from notes.models import Content, Note


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


class NoteCreateAPIView(BaseCreatorCreateAPIView):
    """allows to create note to the user.

    Parameters
    ----------
    BaseCreatorCreateAPIView : cls
        The view allows to create-only endpoint to the user

    """

    querset = Note.objects.all()
    serializer_class = NoteCreateSerializer


class NoteUpdateAPIView(BaseCreatorUpdateAPIView):
    """allow to update note to the user.

    Parameters
    ----------
    BaseCreatorUpdateAPIView : cls
        The view allow update-only endpoint
        for a single model instance

    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializerAfterEnroll


class NoteDestroyAPIView(DestroyAPIView):
    """allow to destroy content to the user.

    Parameters
    ----------
    DestroyAPIView : cls
        The view allow for delete-only
        endpoints for a single model instance

    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializerAfterEnroll
    permission_classes = [IsAuthenticated]


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

    queryset = Content.objects.all()
    serializer_class = ContentSerializerAfterEnroll


class ContentCreateAPIView(BaseCreatorCreateAPIView):
    """allows to create content to the user.

    Parameters
    ----------
    BaseCreatorCreateAPIView : cls
        The view allows to create-only endpoint to the user

    """

    queryset = Content.objects.all()
    serializer_class = ContentCreateSerializer


class ContentUpdateAPIView(BaseCreatorUpdateAPIView):
    """allow to update content to the user.

    Parameters
    ----------
    BaseCreatorUpdateAPIView : cls
        The view allow update-only endpoint
        for a single model instance

    """

    queryset = Content.objects.all()
    serializer_class = ContentSerializerAfterEnroll


class ContentDestroyAPIView(DestroyAPIView):
    """allow to destroy content to the user.

    Parameters
    ----------
    DestroyAPIView : cls
        The view allow for delete-only endpoints
        for a single model instance

    """

    queryset = Content.objects.all()
    serializer_class = ContentSerializerAfterEnroll
    permission_classes = [IsAuthenticated]
