from rest_framework.generics import DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from enrollments.api_admin.serializers import (
    SessionAdminSerializer,
    SessionAdminUpdateSerializer,
)
from enrollments.models import Session


class SessionCreateAPIView(BaseCreatorCreateAPIView):
    """Create a new session for an exam."""

    serializer_class = SessionAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class SessionUpdateAPIView(BaseCreatorUpdateAPIView):
    """Update an existing session for an exam."""

    serializer_class = SessionAdminUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Session.objects.all()


class SessionListAPIView(ListAPIView):
    """List all sessions for an exam."""

    serializer_class = SessionAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Session.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(exam__id=self.kwargs["exam_id"])


class SessionDeleteAPIView(DestroyAPIView):
    """Delete an existing session for an exam."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Session.objects.all()
