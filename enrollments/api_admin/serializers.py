from django.core.exceptions import ValidationError
from rest_framework import serializers

from common.api.serializers import CreatorSerializer, DynamicFieldsCategorySerializer
from enrollments.models import ExamSession, ExamThroughEnrollment


class SessionAdminSerializer(
    DynamicFieldsCategorySerializer,
    CreatorSerializer,
):
    """Serializer for Session create."""

    name = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = ExamSession
        fields = CreatorSerializer.Meta.fields + (
            "start_date",
            "end_date",
            "status",
            "exam",
            "name",
            "result_is_published",
            "result_publish_date",
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
        model = ExamSession
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

    class Meta:
        model = ExamThroughEnrollment

        fields = (
            "id",
            "enrollment",
            "question_states",
            "exam",
            "score",
            "status",
        )

    @staticmethod
    def get_question_states(obj):
        return obj.question_states.all().count()
