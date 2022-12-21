from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from accounts.api.serializers import FullNameField
from accounts.models import Profile
from courses.api_admin.serializers import CourseCategorySerializer

User = get_user_model()


class UserMiniAdminSerializer(serializers.ModelSerializer):
    fullName = FullNameField(source="*")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "fullName",
        ]


class ProfileAdminCreateSerializer(serializers.ModelSerializer):
    """Serializer for the Profile Create Model."""

    class Meta:
        model = Profile
        fields = [
            "college_name",
            "image",
            "qr_code",
            "date_of_birth",
            "faculty",
            "address",
            "interests",
        ]


class ProfileAdminListSerializer(serializers.ModelSerializer):
    """Serializer for the Profile List Model."""

    interests = CourseCategorySerializer(many=True)

    class Meta:
        model = Profile
        fields = [
            "college_name",
            "image",
            "qr_code",
            "date_of_birth",
            "faculty",
            "address",
            "interests",
        ]


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
            "roles",
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
            interests = None
            if "interests" in profile_data:
                interests = profile_data.pop("interests")
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            if interests:
                instance.profile.interests.set(interests)
            instance.profile.save()
        return instance


class UserStudentCreateAdminSerializer(UserCreateAdminSerializer):
    """Admin Student Create Serializer."""

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "fullName",
            "profile",
        ]


class UserListAdminSerializer(serializers.ModelSerializer):
    """Admin List Serializer."""

    fullName = FullNameField(source="*")
    profile = ProfileAdminListSerializer(required=False)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "fullName",
            "roles",
            "profile",
            "is_active",
            "date_joined",
        ]

    def get_roles(self, obj):
        return obj.get_roles()


class UserRetrieveAdminSerializer(serializers.ModelSerializer):
    """Admin Retrieve Serializer."""

    fullName = FullNameField(source="*")
    profile = ProfileAdminListSerializer(required=False)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "roles",
            "fullName",
            "profile",
            "is_active",
        ]

    def get_roles(self, obj):
        return obj.get_roles()


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
            "roles",
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
            if "interests" in profile_data:
                interests = profile_data.pop("interests")
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            if interests:
                instance.profile.interests.set(interests)
            instance.profile.save()
        return instance


class SMSCreditAdminSerializer(serializers.Serializer):
    credit = serializers.IntegerField()
