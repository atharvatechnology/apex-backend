from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from notes.api.serializers import (
    ContentSerializerAfterEnroll,
    ContentSerializerBeforeEnroll,
    NoteSerializerAfterEnroll,
    NoteSerializerBeforeEnroll,
)
from notes.models import Content, Note


# Start Note API
class NoteListAPIVew(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializerAfterEnroll
    filter_backends = [SearchFilter]
    search_fields = ["title"]


class NoteRetrieveAPIViewAfterEnroll(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializerAfterEnroll
    filter_backends = [SearchFilter]
    search_fields = ["title"]


class NoteRetrieveAPIViewBeforeEnroll(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializerBeforeEnroll
    filter_backends = [SearchFilter]
    search_fields = ["title"]


class NoteCreateAPIView(BaseCreatorCreateAPIView):
    querset = Note.objects.all()
    serializer_class = NoteSerializerAfterEnroll


class NoteUpdateAPIView(BaseCreatorUpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializerAfterEnroll


class NoteDestroyAPIView(DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializerAfterEnroll
    permission_classes = [IsAuthenticated]


# End Note API


# Start Content API
class ContentListAPIView(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializerAfterEnroll
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["type"]


class ContentRetrieveAPIViewBeforeEnroll(RetrieveAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializerBeforeEnroll
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["type"]


class ContentRetrieveAPIViewAfterEnroll(RetrieveAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializerAfterEnroll
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["type"]


class ContentCreateAPIView(BaseCreatorCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializerAfterEnroll


class ContentUpdateAPIView(BaseCreatorUpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializerAfterEnroll


class ContentDestroyAPIView(DestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializerAfterEnroll
    permission_classes = [IsAuthenticated]
