from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from courses.api.paginations import StandardResultsSetPagination
from notes.api_admin.serializers import (
    ContentSerializer,
    NoteSerializer,
    RecordedVideoSerializer,
)
from notes.models import Content, Note, RecordedVideo


class NoteCreateAPIView(BaseCreatorCreateAPIView):
    """allows to create note to the user.

    Parameters
    ----------
    BaseCreatorCreateAPIView : cls
        The view allows to create-only endpoint to the user

    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = NoteSerializer


class NoteListAPIView(ListAPIView):
    """permits to list data of notes.

    Parameters
    ----------
    ListAPIView : cls
        The view provides read-only endpoints
        to represent a collection of model instances

    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        queryset = super().get_queryset()
        return queryset.filter(course=course_id)


class NoteRetrieveAPIView(RetrieveAPIView):
    """Allows every detail data of notes.

    Parameters
    ----------
    RetrieveAPIView : cls

        The view allows to view a single
        data of particular list view after
        the user get enrolled

    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteUpdateAPIView(BaseCreatorUpdateAPIView):
    """allow to update note to the user.

    Parameters
    ----------
    BaseCreatorUpdateAPIView : cls
        The view allow update-only endpoint
        for a single model instance

    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteDestroyAPIView(DestroyAPIView):
    """allow to destroy content to the user.

    Parameters
    ----------
    DestroyAPIView : cls
        The view allow for delete-only
        endpoints for a single model instance

    """

    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]


class ContentCreateAPIView(BaseCreatorCreateAPIView):
    """allows to create content to the user.

    Parameters
    ----------
    BaseCreatorCreateAPIView : cls
        The view allows to create-only endpoint to the user

    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ContentSerializer


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ContentSerializer
    pagination_class = StandardResultsSetPagination


class ContentRetrieveAPIView(RetrieveAPIView):
    """permits unrestricted detail data of content.

    Parameters
    ----------
    RetrieveAPIView : cls
        The view allows to view a single
        data of particular list view
        without the user getting enrolled

    """

    queryset = Content.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ContentSerializer


class ContentUpdateAPIView(BaseCreatorUpdateAPIView):
    """allow to update content to the user.

    Parameters
    ----------
    BaseCreatorUpdateAPIView : cls
        The view allow update-only endpoint
        for a single model instance

    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentDestroyAPIView(DestroyAPIView):
    """allow to destroy content to the user.

    Parameters
    ----------
    DestroyAPIView : cls
        The view allow for delete-only endpoints
        for a single model instance

    """

    queryset = Content.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]


class RecordedVideoCreateAPIView(BaseCreatorCreateAPIView):
    """allows to create RecordedVideo to the user.

    Parameters
    ----------
    BaseCreatorCreateAPIView : cls
        The view allows to create-only endpoint to the user

    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = RecordedVideoSerializer


class RecordedVideoListAPIView(ListAPIView):
    """permits to list data of RecordedVideos.

    Parameters
    ----------
    ListAPIView : cls
        The view provides read-only endpoints
        to represent a collection of model instances

    """

    queryset = RecordedVideo.objects.all()
    serializer_class = RecordedVideoSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        queryset = super().get_queryset()
        return queryset.filter(course=course_id)


class RecordedVideoRetrieveAPIView(RetrieveAPIView):
    """Allows every detail data of RecordedVideo.

    Parameters
    ----------
    RetrieveAPIView : cls

        The view allows to view a single
        data of particular list view after
        the user get enrolled

    """

    queryset = RecordedVideo.objects.all()
    serializer_class = RecordedVideoSerializer


class RecordedVideoUpdateAPIView(BaseCreatorUpdateAPIView):
    """allow to update RecordedVideo to the user.

    Parameters
    ----------
    BaseCreatorUpdateAPIView : cls
        The view allow update-only endpoint
        for a single model instance

    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = RecordedVideo.objects.all()
    serializer_class = RecordedVideoSerializer


class RecordedVideoDestroyAPIView(DestroyAPIView):
    """allow to destroy content to the user.

    Parameters
    ----------
    DestroyAPIView : cls
        The view allow for delete-only
        endpoints for a single model instance

    """

    queryset = RecordedVideo.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
