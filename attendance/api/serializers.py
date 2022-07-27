from django.db import transaction
from django.shortcuts import get_object_or_404
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

    # TeacherAttendance = TeacherAttendanceCreateSerializer(required = False)

    class Meta:
        model = TeacherAttendanceDetail
        fields = (
            "id",
            "number_of_period",
            "message",
            "remarks",
            "status",
            # "teacher_attendance",
            # "TeacherAttendance",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)

    # @transaction.atomic
    # def create(self, validated_data):
    #     TeacherAttendance_data = None
    #     if "TeacherAttendanace" in validated_data:
    #         print("hello inside if")
    #         TeacherAttendance_data = validated_data.pop("TeacherAttendance")
    #         print(TeacherAttendance_data)
    #     instance = super().create(validated_data)

    #     if TeacherAttendance_data:
    #         for attr, value in TeacherAttendance_data.items():
    #             setattr(instance.details, attr, value)
    #         instance.details.save()
    #     return instance


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
        # read_only_fields = ("id", "date", "user")

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
        instance = super().update(instance, validated_data)
        teacher_attendance_detail_data = None
        # instance.detail = validated_data.get("details", instance.details)
        if "details" in validated_data:
            teacher_attendance_detail_data = validated_data.pop("details")

        instance = super().update(validated_data)

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

    def validate(self, attrs):
        details = attrs.get("details")
        attrs["details"] = get_object_or_404(TeacherAttendanceDetail, details=details)
        # attrs["details"] = details
        return attrs


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
