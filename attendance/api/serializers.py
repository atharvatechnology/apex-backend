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
            # for attr, value in teacher_attendance_detail_data.items():
            #     setattr(instance.details, attr, value)
            # instance.details.save()
        return instance


class TeacherAttendanceDetailRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving teacher attendance detail model."""

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

    def update(self, instance, validated_data):
        teacher_attendance_detail_data = None
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
        return instance


class TeacherAttendanceDetailDeleteSerializer(serializers.ModelSerializer):
    """Serializer for deleting teacher attendance detail model."""

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
