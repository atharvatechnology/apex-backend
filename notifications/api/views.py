from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from common.paginations import StandardResultsSetPagination
from notifications.api.serializers import NotificationSerializer
from notifications.models import NotificationMessage


class NotificationListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = NotificationMessage.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
