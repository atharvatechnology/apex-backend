from rest_framework import serializers

from attendance.models import StudentAttendance, TeacherAttendance


class StudentAttendanceAdminListSerializer(serializers.ModelSerializer):
    """Serializer for listing admin student attendance model."""

    class Meta:
        model = StudentAttendance
        fields = (
            "id",
            "date",
            "user",
        )


class TeacherAttendanceAdminListSerializer(serializers.ModelSerializer):
    """Serializer for listing admin teacher attendance models."""

    class Meta:
        model = TeacherAttendance
        fields = "__all__"
