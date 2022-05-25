from rest_framework import serializers

from common.api.serializers import CreatorSerializer
from exams.models import Exam, ExamTemplate, Option, Question


class ExamTemplateSerializer(CreatorSerializer):
    class Meta:
        model = ExamTemplate
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "full_marks",
            "pass_marks",
            "duration",
            "display_num_questions",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields


class ExamTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTemplate
        fields = (
            "id",
            "duration",
            "full_marks",
        )


class ExamRetrieveSerializer(CreatorSerializer):
    template = ExamTemplateSerializer()

    class Meta:
        model = Exam
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "category",
            "status",
            "price",
            "template",
        )


class ExamCreateSerializer(CreatorSerializer):
    class Meta:
        model = Exam
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "category",
            "status",
            "price",
            "template",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)


class ExamListSerializer(serializers.ModelSerializer):
    template = ExamTemplateListSerializer()

    class Meta:
        model = Exam
        fields = (
            "id",
            "name",
            "category",
            "status",
            "price",
            "template",
        )


class ExamUpdateSerializer(CreatorSerializer):
    class Meta:
        model = Exam
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "category",
            "status",
            "price",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            "id",
            "detail",
            "correct",
            "img",
        )


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "detail",
            "img",
            "feedback",
            "options",
        )


class ExamPaperSerializer(serializers.ModelSerializer):
    template = ExamTemplateSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = (
            "id",
            "name",
            "category",
            "status",
            "price",
            "questions",
            "template",
        )
