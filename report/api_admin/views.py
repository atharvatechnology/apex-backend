from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from report.api_admin.serializers import GeneratedReportRetrieveSerializer
from report.models import GeneratedReport


class GeneratedReportRetrieveAPIView(RetrieveAPIView):
    """List all generated report location."""

    serializer_class = GeneratedReportRetrieveSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = GeneratedReport.objects.all()
