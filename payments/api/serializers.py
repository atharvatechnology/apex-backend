from rest_framework import serializers

from payments.models import BankPayment, OnlinePayment

# class PaymentCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = (
#             'amount',
#             'enrollment',
#             'status'
#         )


class OnlinePaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlinePayment
        fields = (
            "id",
            "amount",
            "enrollment",
            "variant",
            "tax_amount",
            "service_charge",
            "delivery_charge",
            "merchant_code",
            "product_code",
            "created_at",
            "updated_at",
        )


class BankPaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankPayment
        fields = (
            "id",
            "amount",
            "enrollment",
            "created_at",
            "voucher",
        )


class OnlinePaymentUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.transaction_code = validated_data["transaction_code"]
        instance.product_code = validated_data["product_code"]
        # instance.amount = validated_data['amount']
        instance.status = validated_data["status"]
        instance.capture(validated_data["amount"])
        return instance
        # return super().update(instance, validated_data)

    class Meta:
        model = OnlinePayment
        fields = (
            "product_code",
            "amount",
            "transaction_code",
            "status",
        )
