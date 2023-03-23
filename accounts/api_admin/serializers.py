from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import serializers

from accounts.api.serializers import FullNameField
from accounts.models import Profile
from stafftracking.api_admin.serializers import StaffConnectionStatusUserSerializer

User = get_user_model()


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

    interests = serializers.SerializerMethodField()

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

    def get_interests(self, obj):
        from courses.api_admin.serializers import CourseCategorySerializer

        return CourseCategorySerializer(instance=obj.interests.all(), many=True).data


class UserMiniAdminSerializer(serializers.ModelSerializer):
    fullName = FullNameField(source="*")
    profile = ProfileAdminListSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "fullName",
            "profile",
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


class UserTeacherCreateAdminSerializer(UserCreateAdminSerializer):
    """Admin Teacher Create Serializer."""

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

        roles = validated_data.get("roles", [])
        for role in roles:
            group, _ = Group.objects.get_or_create(name=role)
            instance.groups.add(group)

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


class UserTrackableListSerializer(serializers.ModelSerializer):
    """Serializer fstaffconnectionstatusor the User Trackable List Model."""

    staffconnectionstatus = StaffConnectionStatusUserSerializer()
    fullName = FullNameField(source="*")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "fullName",
            "is_active",
            "staffconnectionstatus",
        ]
