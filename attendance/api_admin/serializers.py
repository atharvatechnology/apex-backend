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


# class StudentAttendanceAdminRetrieveSerializer(serializers.ModelSerializer):
#     """Serializer for retrieving admin student attendance model."""

#     class Meta:
#         model = StudentAttendance
#         fields = (
#             "id",
#             "date",
#             "user",
#         )


class TeacherAttendanceAdminListSerializer(serializers.ModelSerializer):
    """Serializer for listing admin teacher attendance models."""

    # details = TeacherAttendanceDetailCreateSerializer(required=False)

    class Meta:
        model = TeacherAttendance
        fields = (
            "id",
            "name",
            "date",
            "user",
            # "details",
        )


# class TeacherAttendanceAdminRetrieveSerializer(serializers.ModelSerializer):
#     """Serializer for retrieving admin teacher attendance."""

#     class Meta:
#         model = TeacherAttendance
#         fields = (
#             "id",
#             "name",
#             "date",
#             "user",
#         )
