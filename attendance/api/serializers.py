from django.db import transaction
from rest_framework import serializers

from attendance.models import Attendance, TeacherAttendance, TeacherAttendanceDetail
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
