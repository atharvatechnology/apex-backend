from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from meetings.api_admin.serializers import (
    MeetingCreateSerializer,
    MeetingSerializer,
    SubjectCRUDSerializer,
)
from meetings.models import Meeting, Subject
from meetings.providers.register import provider_factory


class MeetingCreateAPIView(CreateAPIView):
    serializer_class = MeetingCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class MeetingDeleteAPIView(DestroyAPIView):
    queryset = Meeting.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_destroy(self, instance):
        variant = instance.variant
        meeting_provider = provider_factory.get_provider(
            variant, name=f"{variant} meeting"
        )
        delete_info = meeting_provider.delete_meeting(instance.meeting_id)
        print(delete_info)
        return super().perform_destroy(instance)


class MeetingListAPIView(ListAPIView):
    queryset = Meeting.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = MeetingSerializer

    def get_queryset(self):
        return super().get_queryset().filter(course_session=self.kwargs["session_id"])


class SubjectCreateAPIView(CreateAPIView):
    """View for creating subjects."""

    serializer_class = SubjectCRUDSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class SubjectListAPIView(ListAPIView):
    """View for listing subjects."""

    serializer_class = SubjectCRUDSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Subject.objects.all()


class SubjectRetrieveAPIView(RetrieveAPIView):
    """View for retrieving subjects."""

    serializer_class = SubjectCRUDSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Subject.objects.all()


class SubjectUpdateAPIView(UpdateAPIView):
    """View for updating subjects."""

    serializer_class = SubjectCRUDSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Subject.objects.all()


class SubjectDeleteAPIView(DestroyAPIView):
    """View for deleting subjects."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Subject.objects.all()
