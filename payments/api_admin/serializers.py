from rest_framework import serializers

from enrollments.api.serializers import EnrollmentPaymentSerializer
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    enrollment = EnrollmentPaymentSerializer()

    class Meta:
        model = Payment
        fields = (
            "id",
            "amount",
            "enrollment",
            "status",
            "created_at",
        )
