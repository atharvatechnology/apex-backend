from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.models import Profile

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


class ProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""

    class Meta:
        model = Profile
        fields = ["college_name", "image", "date_of_birth", "faculty"]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model Update."""

    college_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    class Meta:
        model = Profile
        fields = [
            "college_name",
            "image",
            "date_of_birth",
            "faculty",
            "address",
            "qr_code",
        ]
        read_only_fields = ("qr_code",)


class UserCreateSerializer(serializers.ModelSerializer):
    """User Create Serializer."""

    fullName = FullNameField(source="*")
    profile = ProfileCreateSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "fullName",
            "profile",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def create(self, validated_data):
        profile_data = None
        if "profile" in validated_data:
            profile_data = validated_data.pop("profile")

        instance = super().create(validated_data)
        instance.is_active = False
        instance.set_password(validated_data["password"])
        instance.generate_otp()
        instance.save()

        if profile_data:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
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
    full_name = serializers.SerializerMethodField(read_only=True)
    admin_user = serializers.SerializerMethodField(read_only=True)
    roles = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        extra_fields = UserDetailsSerializer.Meta.extra_fields + [
            "full_name",
            "admin_user",
            "roles",
        ]
        fields = list(UserDetailsSerializer.Meta.fields) + [
            "full_name",
            "admin_user",
            "roles",
        ]

    def get_roles(self, obj):
        return obj.get_roles()

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_admin_user(self, obj):
        return obj.is_superuser


class UserDetailSerializer(UserCustomDetailsSerializer):
    """User Details Serializer."""

    profile = ProfileUpdateSerializer(required=False)

    class Meta(UserCustomDetailsSerializer.Meta):
        fields = list(UserCustomDetailsSerializer.Meta.fields) + ["profile"]
        extra_fields = list(UserCustomDetailsSerializer.Meta.extra_fields) + [
            "profile",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """User Update Serializer."""

    fullName = FullNameField(source="*")
    profile = ProfileUpdateSerializer(required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "fullName",
            "profile",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = None
        if "profile" in validated_data:
            profile_data = validated_data.pop("profile")

        instance = super().update(instance, validated_data)
        instance.save()

        if profile_data:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
        return instance


class StudentQRSerializer(serializers.ModelSerializer):
    """Serializer to provide QR of student."""

    class Meta:
        model = Profile
        fields = ["qr_code"]


class UserMiniSerializer(serializers.ModelSerializer):
    """User Mini Serializer."""

    fullName = FullNameField(source="*")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "fullName",
        ]
