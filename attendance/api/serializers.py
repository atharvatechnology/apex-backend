from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from attendance.models import (
    StudentAttendance,
    TeacherAttendance,
    TeacherAttendanceDetail,
)
from common.api.serializers import CreatorSerializer
from common.utils import decode_user
from courses.models import CourseStatus
from enrollments.models import CourseThroughEnrollment

User = get_user_model()


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
                    enrollment__student=user, courses__status=CourseStatus.INSESSION
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


class StudentAttendanceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating attendance model."""

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
        fields = (
            "id",
            "number_of_period",
            "message",
            "remarks",
            "status",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)


class TeacherAttendanceCreateSerializer(CreatorSerializer):
    """Serializer for creating teacher attendance model."""

    details = TeacherAttendanceDetailCreateSerializer(required=False)

    class Meta:
        model = TeacherAttendance
        fields = (
            "id",
            "name",
            "date",
            "user",
            "details",
        )

    @transaction.atomic
    def create(self, validated_data):
        teacher_attendance_detail_data = None
        if "details" in validated_data:
            teacher_attendance_detail_data = validated_data.pop("details")

        instance = super().create(validated_data)

        if teacher_attendance_detail_data:
            teacher_detail = TeacherAttendanceDetail.objects.create(
                teacher_attendance=instance,
                created_by=instance.user,
                updated_by=instance.user,
                **teacher_attendance_detail_data
            )
            instance.details = teacher_detail
            instance.save()
        return instance


# class TeacherAttendanceDetailRetrieveSerializer(serializers.ModelSerializer):
#     """Serializer for retrieving teacher attendance detail model."""

#     class Meta:
#         model = TeacherAttendanceDetail
#         fields = (
#             "id",
#             "number_of_period",
#             "message",
#             "remarks",
#             "status",
#             "teacher_attendance",
#         )


class TeacherAttendanceDetailUpdateSerializer(CreatorSerializer):
    """Serializer for updating teacher attendance detail model."""

    class Meta:
        model = TeacherAttendanceDetail
        fields = (
            "id",
            "number_of_period",
            "message",
            "remarks",
            "status",
            "teacher_attendance",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)


class TeacherAttendanceUpdateSerializer(CreatorSerializer):
    """Serializer for updating teacher attendance model."""

    details = TeacherAttendanceDetailUpdateSerializer(required=False)

    class Meta:
        model = TeacherAttendance
        fields = (
            "id",
            "name",
            "date",
            "user",
            "details",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        teacher_attendance_detail_data = None
        if "details" in validated_data:
            teacher_attendance_detail_data = validated_data.pop("details")

        instance = super().update(instance, validated_data)

        teacher_attendance_detail_object = hasattr(instance, "details")

        if teacher_attendance_detail_data:
            if teacher_attendance_detail_object:

                for attrs, value in teacher_attendance_detail_data.items():
                    setattr(instance.details, attrs, value)
                instance.details.save()
            else:
                instance = TeacherAttendanceDetail.objects.create(
                    teacher_attendance=instance,
                    created_by=instance.user,
                    updated_by=instance.user,
                    **teacher_attendance_detail_data
                )

                instance.save()

        return instance


class TeacherAttendanceRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving teacher attendance models."""

    details = TeacherAttendanceDetailCreateSerializer(required=False)

    class Meta:
        model = TeacherAttendance
        # field = (
        #     "id",
        #     "name",
        #     "date",
        #     "user",
        #     "details",
        # )
        fields = "__all__"
