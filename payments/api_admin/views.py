from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from common.paginations import StandardResultsSetPagination
from common.permissions import IsAccountant, IsSuperAdminorDirector
from payments import PaymentStatus
from payments.api_admin.filters import PaymentFilter
from payments.api_admin.serializers import PaymentSerializer
from payments.models import Payment


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.filter(status=PaymentStatus.PAID)
    permission_classes = [IsSuperAdminorDirector | IsAccountant]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
