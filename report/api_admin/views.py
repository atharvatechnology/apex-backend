from rest_framework.generics import RetrieveAPIView

from common.permissions import IsAccountant, IsAdminOrSuperAdminOrDirector
from report.api_admin.serializers import GeneratedReportRetrieveSerializer
from report.models import GeneratedReport


class GeneratedReportRetrieveAPIView(RetrieveAPIView):
    """List all generated report location."""

    serializer_class = GeneratedReportRetrieveSerializer
    permission_classes = [IsAccountant | IsAdminOrSuperAdminOrDirector]
    queryset = GeneratedReport.objects.all()
