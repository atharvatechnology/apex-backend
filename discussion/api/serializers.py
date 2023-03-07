from rest_framework import serializers

from accounts.api_admin.serializers import UserMiniAdminSerializer
from common.api.serializers import CreatorSerializer
from discussion.models import Question


class ReplySerializer(serializers.ModelSerializer):
    created_by = UserMiniAdminSerializer()

    class Meta:
        model = Question
        fields = ["id", "question", "content", "created_by", "created_at"]


class QuestionListSerializer(serializers.ModelSerializer):
    """Serializer to list all the questions."""

    created_by = UserMiniAdminSerializer()
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        ref_name = "Discussion Question"
        model = Question

        fields = ["id", "content", "replies", "reply_count", "created_by", "created_at"]


class QuestionRetrieveSerializer(serializers.ModelSerializer):
    """Serializer to retrieve a question."""

    created_by = UserMiniAdminSerializer()
    replies = QuestionListSerializer(many=True, read_only=True)
    question = QuestionListSerializer(read_only=True)

    class Meta:
        ref_name = "Discussion Question"
        model = Question
        fields = [
            "id",
            "content",
            "question",
            "reply_count",
            "replies",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]


class QuestionCreateSerializer(CreatorSerializer):
    """Serializer to create question."""

    class Meta:
        ref_name = "Discussion Question"
        model = Question
        fields = ["content", "question"]

    def create(self, validated_data):
        question = validated_data.get("question")
        if (question is not None) and question.is_question is False:
            raise serializers.ValidationError(
                "Reply for Answer is not Possible",
            )
        else:
            return Question.objects.create(**validated_data)


class QuestionUpdateSerializer(CreatorSerializer):
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
