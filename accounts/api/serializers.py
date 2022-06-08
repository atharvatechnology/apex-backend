from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class FullNameField(serializers.Field):
    """Custom Full Name field for the User model."""

    def to_representation(self, value):
        """Return the full name of the user."""
        return value.get_full_name()

    def to_internal_value(self, data):
        """Return the user object fields based on the full name."""
        try:
            fname, lname = data.rsplit(" ", 1)
        except ValueError:
            fname, lname = data, ""
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

    def validate(self, attrs):
        username = attrs.get("username")
        attrs["user"] = get_object_or_404(User, username=username)
        return attrs


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

    def validate(self, attrs):
        username = attrs.get("username")
        attrs["user"] = get_object_or_404(User, username=username)
        return attrs


class UserCustomDetailsSerializer(UserDetailsSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        extra_fields = UserDetailsSerializer.Meta.extra_fields + ["full_name"]
        fields = list(UserDetailsSerializer.Meta.fields) + ["full_name"]

    def get_full_name(self, obj):
        return obj.get_full_name()
