from django.core.exceptions import ValidationError
from rest_framework import serializers

from common.api.serializers import (
    CreatorSerializer,
    DynamicFieldsCategorySerializer,
    PublishedSerializer,
)
from enrollments.api.serializers import ExamEnrollmentSerializer
from enrollments.models import Enrollment, ExamThroughEnrollment, Session


class SessionAdminSerializer(
    CreatorSerializer, DynamicFieldsCategorySerializer, PublishedSerializer
):
    """Serializer for Session create."""

    name = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Session
        fields = (
            CreatorSerializer.Meta.fields
            + PublishedSerializer.Meta.fields
            + (
                "start_date",
                "end_date",
                "status",
                "exam",
                "name",
            )
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + (
            "status",
            "end_date",
        )

    def create(self, validated_data):
        """Create a new Session.

        checks full_clean of model and raises ValidationError if any errors
        """
        try:
            instance = super().create(validated_data)
            instance.full_clean()
        except ValidationError as error:
            raise serializers.ValidationError(
                serializers.as_serializer_error(error)
            ) from error
        return instance


class SessionAdminUpdateSerializer(SessionAdminSerializer):
    """Serializer for Session update."""

    class Meta:
        model = Session
        fields = SessionAdminSerializer.Meta.fields
        read_only_fields = SessionAdminSerializer.Meta.read_only_fields + (
            "start_date",
            "end_date",
            "exam",
        )

    def update(self, instance, validated_data):
        """Update an existing Session.

        checks full_clean of model and raises ValidationError if any errors
        """
        try:
            instance = super().update(instance, validated_data)
            instance.full_clean()
        except ValidationError as error:
            raise serializers.ValidationError(
                serializers.as_serializer_error(error)
            ) from error
        return instance


class ExamThroughEnrollmentAdminListSerializer(serializers.ModelSerializer):
    """Serializer for ExamThroughEnrollment List."""

    question_states = serializers.SerializerMethodField()
    rank = serializers.ReadOnlyField()
    enrollment = serializers.SerializerMethodField()

    class Meta:
        model = ExamThroughEnrollment

        fields = (
            "id",
            "enrollment",
            "question_states",
            "exam",
            "score",
            "status",
            "rank",
        )

    @staticmethod
    def get_enrollment(obj):
        if obj.enrollment.student.last_name != "":
            return (
                obj.enrollment.student.first_name
                + " "
                + obj.enrollment.student.last_name
            )
        else:
            return obj.enrollment.student.first_name

    @staticmethod
    def get_question_states(obj):
        return obj.question_states.all().count()


class ExamEnrollmentCreateSerializer(serializers.ModelSerializer):
    exams = ExamEnrollmentSerializer(many=True, source="exam_enrolls", required=False)

    class Meta:
        model = Enrollment
        fields = (
            "student",
            "exams",
        )
