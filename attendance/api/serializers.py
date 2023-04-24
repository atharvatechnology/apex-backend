from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from attendance.models import (
    Attendance,
    StudentAttendance,
    TeacherAttendance,
    TeacherAttendanceDetail,
)
from common.api.serializers import CreatorSerializer
from common.utils import decode_user
from courses.models import CourseStatus
from enrollments.models import CourseThroughEnrollment

User = get_user_model()


class AttendanceCreateSerializer(CreatorSerializer):
    """Serializer for creating attendance."""

    class Meta:
        model = Attendance
        fields = "__all__"


class StudentOnlineAttendanceSerializer(CreatorSerializer):
    """Serializer for creating attendance for online student."""

    class Meta:
        model = StudentAttendance
        fields = (
            "id",
            "date",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class StudentAttendanceCreateSerializer(CreatorSerializer):
    """Serializer for creating attendance model."""

    user = serializers.CharField()

    class Meta:
        model = StudentAttendance
        fields = (
            "id",
            "date",
            "user",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    def validate_user(self, value):
        decoded_user = decode_user(value)
        if decoded_user is not None:
            user = User.objects.filter(username=decoded_user).first()
            enrolled_student = (
                CourseThroughEnrollment.objects.filter(
                    enrollment__student=user, course__status=CourseStatus.INSESSION
                )
                or None
            )
            if enrolled_student is not None:
                return user
            else:
                raise serializers.ValidationError(
                    "Student is not enrolled in any course."
                )
        raise serializers.ValidationError("Invalid user")

    def validate(self, value):
        attendance = StudentAttendance.objects.filter(
            user=value["user"], date__date=value["date"]
        )
        if attendance.exists():
            raise serializers.ValidationError("Attendance already exists.")
        return value


class StudentAttendanceRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving attendance model."""

    class Meta:
        model = StudentAttendance
        fields = (
            "id",
            "date",
            "user",
        )


class TeacherAttendanceDetailCreateSerializer(CreatorSerializer):
    """Serializer for creating teacher attendance detail model."""

    class Meta:
        model = TeacherAttendanceDetail
        fields = CreatorSerializer.Meta.fields + (
            "number_of_period",
            "message",
            "remarks",
            "status",
            "section",
            "subject",
            "class_note",
            "start_time",
            "end_time",
            "teacher_attendance",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)


class TeacherAttendanceDetailSerializer(serializers.ModelSerializer):
    """Serializer for listing teacher attendance detail model."""

    class Meta:
        model = TeacherAttendanceDetail
        fields = (
            "id",
            "number_of_period",
            "message",
            "remarks",
            "status",
            "section",
            "subject",
            "class_note",
            "start_time",
            "end_time",
        )


class TeacherAttendanceDetailCreateNestedSerializer(CreatorSerializer):
    """Serializer for creating teacher attendance detail model."""

    class Meta:
        model = TeacherAttendanceDetail
        fields = CreatorSerializer.Meta.fields + (
            "number_of_period",
            "message",
            "remarks",
            "status",
            "section",
            "subject",
            "class_note",
            "start_time",
            "end_time",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)


class TeacherAttendanceCreateSerializer(CreatorSerializer):
    """Serializer for creating teacher attendance model."""

    teacher_details = TeacherAttendanceDetailCreateNestedSerializer(required=False)

    class Meta:
        model = TeacherAttendance
        fields = (
            "id",
            "date",
            "teacher_details",
        )
        extra_kwargs = {
            "teacher_details": {"write_only": True},
        }

    @transaction.atomic
    def create(self, validated_data):
        teacher_attendance_detail_data = None
        if "teacher_details" in validated_data:
            teacher_attendance_detail_data = validated_data.pop("teacher_details")

        instance = super().create(validated_data)

        if teacher_attendance_detail_data:
            TeacherAttendanceDetail.objects.create(
                teacher_attendance=instance,
                created_by=instance.user,
                updated_by=instance.user,
                **teacher_attendance_detail_data
            )
        return instance


class TeacherAttendanceRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving teacher attendance models."""

    class Meta:
        model = TeacherAttendance
        fields = (
            "id",
            "name",
            "date",
            "user",
            "details",
        )
