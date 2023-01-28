from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.api_admin.serializers import UserMiniAdminSerializer
from attendance.models import (
    StudentAttendance,
    TeacherAttendance,
    TeacherAttendanceDetail,
)

User = get_user_model()


class StudentAttendanceAdminListSerializer(serializers.ModelSerializer):
    """Serializer for listing admin student attendance model."""

    user = UserMiniAdminSerializer()

    class Meta:
        model = StudentAttendance
        fields = (
            "id",
            "date",
            "user",
        )


class StudentAttendanceAdminHistoryListSerializer(serializers.ModelSerializer):
    """Serializer for listing history of student attendance model."""

    user = UserMiniAdminSerializer()

    class Meta:
        model = StudentAttendance
        fields = (
            "id",
            "date",
            "user",
        )


class StudentAttendanceAdminRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for updating admin student attendance model."""

    user = UserMiniAdminSerializer()

    class Meta:
        model = StudentAttendance
        fields = (
            "id",
            "date",
            "user",
        )


class StudentAttendanceAdminUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating admin student attendance model."""

    user = UserMiniAdminSerializer(read_only=True)

    class Meta:
        model = StudentAttendance
        fields = (
            "id",
            "date",
            "user",
        )


class TeacherAttendanceDetailAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin detail teacher attendance model."""

    class Meta:
        model = TeacherAttendanceDetail
        fields = (
            "id",
            "section",
            "number_of_period",
            "class_note",
            "start_time",
            "end_time",
            "subject",
            # "teacher_attendance",
        )


class TeacherAttendanceAdminListSerializer(serializers.ModelSerializer):
    """Serializer for listing admin teacher attendance models."""

    user = UserMiniAdminSerializer()
    details = TeacherAttendanceDetailAdminSerializer(read_only=True, many=True)

    class Meta:
        model = TeacherAttendance
        fields = (
            "id",
            "date",
            "user",
            "details",
        )


class TeacherAttendanceAdminHistoryListSerializer(serializers.ModelSerializer):
    """Serializer for listing history of admin teacher attendance models."""

    user = UserMiniAdminSerializer()
    details = TeacherAttendanceDetailAdminSerializer(read_only=True, many=True)

    class Meta:
        model = TeacherAttendance
        fields = (
            "id",
            "date",
            "user",
            "details",
        )


class TeacherAttendanceAdminUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating admin teacher attendance models."""

    user = UserMiniAdminSerializer(read_only=True)
    details = TeacherAttendanceDetailAdminSerializer(read_only=True, many=True)

    class Meta:
        model = TeacherAttendance
        fields = (
            "id",
            "date",
            "user",
            "details",
        )


class TeacherAttendanceAdminRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving admin teacher attendance models."""

    user = UserMiniAdminSerializer()
    details = TeacherAttendanceDetailAdminSerializer(required=False, many=True)

    class Meta:
        model = TeacherAttendance
        fields = (
            "id",
            "date",
            "user",
            "details",
        )
