from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from common.paginations import StandardResultsSetPagination
from payments import PaymentStatus
from payments.api_admin.filters import PaymentFilter
from payments.api_admin.serializers import PaymentSerializer
from payments.models import Payment


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.filter(status=PaymentStatus.PAID)
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
