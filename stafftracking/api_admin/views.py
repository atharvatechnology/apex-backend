from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsSuperAdminOrDirector
from stafftracking.api_admin.serializers import StaffTrackingSerializer
from stafftracking.models import StaffTracking

channel_layer = get_channel_layer()


class StaffTrackingListAPIView(ListAPIView):
    queryset = StaffTracking.objects.all()
    serializer_class = StaffTrackingSerializer
    permission_classes = [IsSuperAdminOrDirector]


class StaffTrackingListPerUserAPIView(ListAPIView):
    queryset = StaffTracking.objects.all()
    serializer_class = StaffTrackingSerializer
    permission_classes = [IsSuperAdminOrDirector]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id", None)
        return super().get_queryset().filter(user=user_id)[:5]


class StaffTrackingRequestAPIView(APIView):
    permission_classes = [IsSuperAdminOrDirector]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        async_to_sync(channel_layer.group_send)(
            f"track_{user_id}",
            {"type": "send_request_user", "status": "asdf"},
        )

        return Response({"msg": "Location has been requested."})
