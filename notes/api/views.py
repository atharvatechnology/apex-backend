from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from notes.api.serializers import ContentSerializer, NoteSerializer
from notes.models import Content, Note


# Start Note API
class NoteListAPIVew(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title"]


class NoteCreateAPIView(BaseCreatorCreateAPIView):
    querset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteUpdateAPIView(BaseCreatorUpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteDestroyAPIView(DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]


# End Note API


# Start Content API
class ContentListAPIView(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["type"]


class ContentCreateAPIView(BaseCreatorCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentUpdateAPIView(BaseCreatorUpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentDestroyAPIView(DestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]
