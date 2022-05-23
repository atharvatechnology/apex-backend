from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.timezone import datetime, make_aware, timedelta
from rest_framework import serializers

from accounts.api.otp import OTP

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.otp_counter += 1
        instance.is_active = False
        instance.set_password(validated_data["password"])
        otp = OTP.generateOTP(instance.username, instance.otp_counter)
        instance.otp = otp
        instance.save()
        OTP.sendOTP(instance.username, otp)
        return instance


class UserOTPVerifySerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "otp",
        ]

    def validate_otp(self, value):
        five_minutes_ago = make_aware(
            datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        )
        if not self.instance.otp:
            raise serializers.ValidationError("OTP is already used")
        if self.instance.otp_generate_time < five_minutes_ago:
            raise serializers.ValidationError("The OTP is out of date ")
        if self.instance.otp != value:
            raise serializers.ValidationError("OTP is not valid")
        return None

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.is_active = True
        instance.save()
        return instance


class UserResetPasswordRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.otp_counter += 1
        otp = OTP.generateOTP(instance.username, instance.otp_counter)
        instance.otp = otp
        instance.otp_generate_time = make_aware(datetime.now())
        instance.save()
        OTP.sendOTP(instance.username, otp)
        return instance


class UserResetPasswordVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "otp",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_otp(self, value):
        five_minutes_ago = make_aware(
            datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        )
        if not self.instance.otp:
            raise serializers.ValidationError("OTP is already used")
        if self.instance.otp_generate_time < five_minutes_ago:
            raise serializers.ValidationError("The OTP is out of date ")
        if self.instance.otp != value:
            raise serializers.ValidationError("OTP is not valid")
        return None

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data["password"])
        instance.is_active = True
        instance.save()
        return instance
