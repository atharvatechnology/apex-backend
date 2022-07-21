from django.utils import timezone
from rest_framework.generics import DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from enrollments.api_admin.serializers import (
    ExamThroughEnrollmentAdminListSerializer,
    SessionAdminSerializer,
    SessionAdminUpdateSerializer,
)
from enrollments.models import Session
from enrollments.models import ExamThroughEnrollment
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from courses.api.paginations import StandardResultsSetPagination


class SessionCreateAPIView(BaseCreatorCreateAPIView):
    """Create a new session for an exam."""

    serializer_class = SessionAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class SessionUpdateAPIView(BaseCreatorUpdateAPIView):
    """Update an existing session for an exam."""

    serializer_class = SessionAdminUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Session.objects.all()

    def can_update_object(self, obj):
        """Check if the user can update the object.

        Raises a PermissionDenied exception
            if the user cannot update a session which is ended.
        """
        if obj.end_date < timezone.now():
            self.permission_denied(
                self.request, message="Cannot update a session which is ended."
            )

    def get_object(self):
        obj = super().get_object()
        self.can_update_object(obj)
        return obj


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

    def can_delete(self, object):
        """Check if the user can delete the object.

        Raises a PermissionDenied exception
            if the user cannot delete a session which is ended.
        """
        if object.start_date < timezone.now():
            self.permission_denied(
                self.request,
                message="Cannot delete a session that has already started.",
            )

    def get_object(self):
        obj = super().get_object()
        self.can_delete(obj)
        return obj


class ExamThroughEnrollmentListAPIView(ListAPIView):
    """List all student in Exam"""
    serializer_class = ExamThroughEnrollmentAdminListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ExamThroughEnrollment.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['exam']
    ordering_fields = ['status', 'score']
    search_fields = ['enrollment__student__username']

