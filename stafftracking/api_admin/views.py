from rest_framework.generics import ListAPIView

from stafftracking.api_admin.serializers import StaffTrackingSerializer
from stafftracking.models import StaffTracking


class StaffTrackingListAPIView(ListAPIView):
    queryset = StaffTracking.objects.all()
    serializer_class = StaffTrackingSerializer
