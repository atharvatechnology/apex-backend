from rest_framework import serializers

from attendance.models import StudentAttendance


class StudentAttendanceAdminRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for listing admin student attendance model."""

    class Meta:
        model = StudentAttendance
        fields = (
            "id",
            "date",
            "user",
        )
