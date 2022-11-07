from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from accounts.api.serializers import FullNameField
from accounts.models import Profile

User = get_user_model()


class ProfileAdminCreateSerializer(serializers.ModelSerializer):
    """Serializer for the Profile Model."""

    class Meta:
        model = Profile
        fields = ["image", "date_of_birth", "faculty", "address"]


class UserCreateAdminSerializer(serializers.ModelSerializer):
    """Admin Create Serializer."""

    fullName = FullNameField(source="*")
    profile = ProfileAdminCreateSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "fullName",
            "profile",
        ]

    @transaction.atomic
    def create(self, validated_data):
        profile_data = None
        if "profile" in validated_data:
            profile_data = validated_data.pop("profile")

        instance = super().create(validated_data)
        instance.is_active = True
        instance.set_password(validated_data["username"])
        instance.save()

        if profile_data:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
        return instance


class UserListAdminSerializer(serializers.ModelSerializer):
    """Admin List Serializer."""

    fullName = FullNameField(source="*")
    profile = ProfileAdminCreateSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "fullName",
            "profile",
            "is_active",
            "date_joined",
        ]


class UserRetrieveAdminSerializer(serializers.ModelSerializer):
    """Admin Retrieve Serializer."""

    fullName = FullNameField(source="*")
    profile = ProfileAdminCreateSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "fullName",
            "profile",
            "is_active",
        ]


class UserUpdateAdminSerializer(serializers.ModelSerializer):
    """Admin Update Serializer."""

    fullName = FullNameField(source="*")
    profile = ProfileAdminCreateSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "fullName",
            "profile",
            "is_active",
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = None
        if "profile" in validated_data:
            profile_data = validated_data.pop("profile")

        instance = super().update(instance, validated_data)
        instance.is_active = True
        instance.save()

        if profile_data:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
        return instance
