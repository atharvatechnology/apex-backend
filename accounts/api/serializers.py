from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

User = get_user_model()


class FullNameField(serializers.Field):
    """Custom Full Name field for the User model."""

    def to_representation(self, value):
        """Return the full name of the user."""
        return value.get_full_name()

    def to_internal_value(self, data):
        """Return the user object fields based on the full name."""
        fname, lname = data.rsplit(" ", 1)
        return {"first_name": fname, "last_name": lname}


class UserCreateSerializer(serializers.ModelSerializer):
    """User Create Serializer."""

    fullName = FullNameField(source="*")

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "fullName",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.is_active = False
        instance.set_password(validated_data["password"])
        instance.generate_otp()
        instance.save()
        return instance


class UserCreateOTPVerifySerializer(serializers.ModelSerializer):
    """User Create OTP Verify Serializer."""

    otp = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "otp",
        ]

    def validate_otp(self, value):
        status, message = self.instance.validate_otp(value)
        if not status:
            raise serializers.ValidationError(message)
        return None

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.is_active = True
        instance.save()
        return instance


class UserResetPasswordOTPRequestSerializer(serializers.ModelSerializer):
    """User Reset Password OTP Request Serializer."""

    class Meta:
        model = User
        fields = [
            "username",
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.generate_otp()
        instance.save()
        return instance


class UserResetPasswordOTPVerifySerializer(serializers.ModelSerializer):
    """User Reset Password OTP Verify Serializer."""

    otp = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "otp",
        ]

    def validate_otp(self, value):
        status, message = self.instance.validate_otp(value)
        if not status:
            raise serializers.ValidationError(message)
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class UserResetPasswordConfirmSerializer(serializers.ModelSerializer):
    """User Reset Password Confirm Serializer."""

    class Meta:
        model = User
        fields = [
            "username",
            "otp",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_otp(self, value):
        status, message = self.instance.validate_otp(value)
        if not status:
            raise serializers.ValidationError(message)
        return None

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data["password"])
        instance.is_active = True
        instance.save()
        return instance
