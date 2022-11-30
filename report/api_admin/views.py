from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from report.api_admin.serializers import GeneratedReportSerializers
from report.models import GeneratedReport


class GeneratedReportListAPIView(ListAPIView):
    """List all generated report location."""

    serializer_class = GeneratedReportSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = GeneratedReport.objects.all()
