from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from accounts.api.serializers import FullNameField
from accounts.models import Profile

User = get_user_model()


class ProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for the Profile Model."""

    class Meta:
        model = Profile
        fields = ["image", "date_of_birth", "faculty", "address", "phone_number"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Admin Create Serializer."""

    fullName = FullNameField(source="*")
    profile = ProfileCreateSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
        ]

    # @transaction.atomic
    # def create(self, validated_data):
    #     instance = super().create(validated_data)
    #     instance.is_active = False
    #     instance.set_password(validated_data["password"])
    #     instance.save()
    #     return instance

    @transaction.atomic
    def create(self, validated_data):
        profile_data = None
        if "profile" in validated_data:
            profile_data = validated_data.pop("profile")
        instance = super().create(validated_data)
        instance.is_active = False
        instance.set_password(validated_data["password"])
        instance.save()
        if profile_data:
            instance.profile.update(**profile_data)
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """Admin List Serializer."""

    fullName = FullNameField(source="*")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "fullName",
        ]
