from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from meetings.api_admin.serializers import MeetingCreateSerializer
from meetings.models import Meeting
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
