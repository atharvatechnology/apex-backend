from rest_framework import serializers

from attendance.models import Attendance, TeacherAttendanceDetail
from common.api.serializers import CreatorSerializer


class AttendanceCreateSerializer(CreatorSerializer):
    """Serializer for creating attendance model."""

    class Meta:
        model = Attendance
        fields = (
            "id",
            "date",
            "user",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class AttendanceRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving attendance model."""

    class Meta:
        model = Attendance
        fields = (
            "id",
            "date",
            "user",
        )


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating attendance model."""

    class Meta:
        model = Attendance
        fields = (
            "id",
            "date",
            "user",
        )


class AttendanceDeleteSerializer(serializers.ModelSerializer):
    """Serializer for deleting attendance model."""

    class Meta:
        model = Attendance
        fields = (
            "id",
            "date",
            "user",
        )


class TeacherAttendanceDetailCreateSerializer(CreatorSerializer):
    """Serializer for creating teacher attendance detail model."""

    class Meta:
        model = TeacherAttendanceDetail
        fields = (
            "id",
            "number_of_peroid",
            "message",
            "remarks",
            "status",
            "teacher_attendance",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class TeacherAttendanceDetailRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving teacher attendance detail model."""

    class Meta:
        model = TeacherAttendanceDetail
        fields = (
            "id",
            "number_of_peroid",
            "message",
            "remarks",
            "status",
            "teacher_attendance",
        )


class TeacherAttendanceDetailUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating teacher attendance detail model."""

    class Meta:
        model = TeacherAttendanceDetail
        fields = (
            "id",
            "number_of_peroid",
            "message",
            "remarks",
            "status",
            "teacher_attendance",
        )


class TeacherAttendanceDetailDeleteSerializer(serializers.ModelSerializer):
    """Serializer for deleting teacher attendance detail model."""

    class Meta:
        model = TeacherAttendanceDetail
        fields = (
            "id",
            "number_of_peroid",
            "message",
            "remarks",
            "status",
            "teacher_attendance",
        )
