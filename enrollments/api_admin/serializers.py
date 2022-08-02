from django.core.exceptions import ValidationError
from rest_framework import serializers

from common.api.serializers import (
    CreatorSerializer,
    DynamicFieldsCategorySerializer,
    PublishedSerializer,
)
from enrollments.api.serializers import ExamEnrollmentSerializer
from enrollments.api.utils import (
    batch_is_enrolled_and_price,
    exam_data_save,
    get_student_rank,
)
from enrollments.models import (
    Enrollment,
    EnrollmentStatus,
    ExamThroughEnrollment,
    Session,
)


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
    rank = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()

    class Meta:
        model = ExamThroughEnrollment

        fields = (
            "id",
            "student",
            "question_states",
            "exam",
            "score",
            "status",
            "rank",
        )

    def get_rank(self, obj):
        return get_student_rank(obj)

    @staticmethod
    def get_student(obj):
        return obj.enrollment.student.__str__()

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

    def create(self, validated_data):
        exams_data = validated_data.pop("exam_enrolls", None)
        user = self.context["request"].user
        total_price = 0.0
        if not exams_data:
            raise serializers.ValidationError("Field should not be empty")

        if exams_data:
            exams = [data.get("exam") for data in exams_data]
            total_price += batch_is_enrolled_and_price(exams, user)
        enrollment = super().create(validated_data)

        exam_data_save(exams_data, enrollment)
        if total_price == 0.0:
            enrollment.status = EnrollmentStatus.ACTIVE
        enrollment.save()
        return enrollment
