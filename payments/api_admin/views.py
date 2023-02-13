from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from common.api.views import BaseReportGeneratorAPIView
from common.paginations import StandardResultsSetPagination
from common.permissions import IsAccountant, IsSuperAdminOrDirector
from payments import PaymentStatus
from payments.api_admin.filters import PaymentFilter
from payments.api_admin.serializers import PaymentSerializer
from payments.models import Payment


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.filter(status=PaymentStatus.PAID)
    permission_classes = [IsSuperAdminOrDirector | IsAccountant]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class PaymentReportGeneratorAPIView(BaseReportGeneratorAPIView):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = PaymentFilter
    queryset = Payment.objects.filter(status=PaymentStatus.PAID)
    model_name = "Payment"

    def get(self, request):
        return Response(
            {
                "model_fields": [
                    "name",
                    "type",
                    "enrollment",
                    "revenue",
                ]
            }
        )
