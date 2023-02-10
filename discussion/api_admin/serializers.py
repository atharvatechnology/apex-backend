from rest_framework import serializers

from common.api.serializers import CreatorSerializer
from discussion.models import Question


class QuestionAdminListSerializer(serializers.ModelSerializer):
    """Serializer to list all the questions."""

    replies = "QuestionAdminListSerializer(many=True,read_only=True)"
    question = "QuestionAdminListSerializer(read_only=True)"

    class Meta:
        ref_name = "Discussion Question"
        model = Question
        fields = ["id", "content", "question", "replies", "created_by", "created_at"]


class QuestionAdminRetrieveSerializer(serializers.ModelSerializer):
    """Serializer to retrieve a question."""

    replies = QuestionAdminListSerializer(many=True, read_only=True)
    question = QuestionAdminListSerializer(read_only=True)

    class Meta:
        ref_name = "Discussion Question"
        model = Question
        fields = [
            "id",
            "content",
            "question",
            "replies",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]


class QuestionAdminCreateSerializer(CreatorSerializer):
    """Serializer to create question."""

    class Meta:
        ref_name = "Discussion Question"
        model = Question
        fields = ["content", "question"]

    def create(self, validated_data):
        question = validated_data.get("question")
        if question is not None and question.is_question is False:
            raise serializers.ValidationError(
                "Reply for Answer is not Possible",
            )
        else:
            return Question.objects.create(**validated_data)


class QuestionAdminUpdateSerializer(CreatorSerializer):
    """Serializer to update question."""

    class Meta:
        ref_name = "Discussion Question"
        model = Question
        fields = ["content"]

    def update(self, instance, validated_data):
        if (instance.question is not None) and instance.question.is_question is False:
            raise serializers.ValidationError(
                "Reply for Answer is not Possible",
            )
        else:
            return super().update(instance, validated_data)
