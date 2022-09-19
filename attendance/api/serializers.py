from django.db import transaction
from rest_framework import serializers

from attendance.models import Attendance, TeacherAttendance, TeacherAttendanceDetail
from common.api.serializers import CreatorSerializer
from common.utils import decode_user
from enrollments.models import Enrollment
from courses.models import CourseStatus


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

    def validate_user(self, value):
        usr_name = value["user"]
        print(usr_name)
        decoded_user = decode_user(usr_name)
        if decoded_user is not None:
            enrolled_student = Enrollment.objects.filter(
                student__username=decoded_user, courses=CourseStatus.INSESSION
            ) or None
            if enrolled_student is not None:
                return value
        raise serializers.ValidationError("Invalid user")
        
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
