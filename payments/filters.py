import django_filters

from payments.models import Payment


class PaymentDateFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {"created_at": ["year"]}
