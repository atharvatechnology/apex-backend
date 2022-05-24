from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from notes.api.serializers import ContentSerializer, NoteSerializer
from notes.models import Content, Note


# Start Note API
class NoteListAPIVew(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteCreateAPIView(CreateAPIView):
    querset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Request user is set as creator and updater automatically."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class NoteUpdateAPIView(UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """Request user is set as updater automatically."""
        serializer.save(updated_by=self.request.user)


class NoteDestroyAPIView(DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]


# End Note API


# Start Content API
class ContentListAPIView(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentCreateAPIView(CreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Request user is set as creator and updater automatically."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class ContentUpdateAPIView(UpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """Request user is set as updater automatically."""
        serializer.save(updated_by=self.request.user)


class ContentDestroyAPIView(DestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]
