from rest_framework import serializers

from enrollments.api.serializers import EnrollmentPaymentSerializer
from payments import PaymentStatus
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


class PaymentCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "amount",
            "enrollment",
            "status",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "status")

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        payment.change_status(PaymentStatus.PAID)
        return payment
