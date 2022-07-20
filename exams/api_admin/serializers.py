from django.db import transaction
from rest_framework import serializers

from common.api.serializers import CreatorSerializer
from enrollments.api.serializers import SessionSerializer
from exams.api.serializers import ExamTemplateListSerializer
from exams.models import (
    Exam,
    ExamImage,
    ExamTemplate,
    ExamTemplateStatus,
    Option,
    Question,
    Section,
)

from .validators import validate_gt_than_template_marks


class OptionBaseSerializer(serializers.ModelSerializer):
    """Base serializer for Option model."""

    class Meta:
        model = Option
        fields = (
            "id",
            "detail",
            "correct",
            "img",
        )


class OptionUpdateOnExamUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Option model when Exam is updated."""

    id = serializers.IntegerField(required=True)

    class Meta:
        model = Option
        fields = (
            "id",
            "detail",
            "correct",
            "img",
        )


class OptionCUDSerializer(OptionBaseSerializer):
    """Serializer for creating options."""

    class Meta:
        model = Option
        fields = OptionBaseSerializer.Meta.fields + ("question",)


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Serializer when admin is creating a question."""

    options = OptionBaseSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "detail",
            "img",
            "exam",
            "section",
            "options",
            "feedback",
        )

    @transaction.atomic
    def create(self, validated_data):
        options = validated_data.pop("options", None)
        num_correct_options = sum(option.get("correct", 0) for option in options)
        if num_correct_options != 1:
            raise serializers.ValidationError("Exactly one option must be correct.")
        if not options:
            raise serializers.ValidationError("Options are required.")
        question = Question.objects.create(**validated_data)
        for option in options:
            Option.objects.create(question=question, **option)
        return question

    # def validate(self, attrs):

    #     return


class QuestionUpdateSerializer(serializers.ModelSerializer):
    """Serializer when admin is updating a question."""

    options = OptionUpdateOnExamUpdateSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "detail",
            "img",
            "exam",
            "section",
            "feedback",
            "options",
        )
        read_only_fields = (
            "id",
            "exam",
            "section",
        )

    def update(self, instance, validated_data):
        options = validated_data.pop("options", None)
        instance = super().update(instance, validated_data)
        instance_options_id = [option.id for option in instance.options.all()]
        if options:
            # check for invalid options data
            for option in options:
                option_id = option.pop("id", None)
                if not option_id:
                    raise serializers.ValidationError(
                        "Please provide id for all options"
                    )
                if option_id not in instance_options_id:
                    raise serializers.ValidationError("Invalid option id")
                Option.objects.filter(id=option_id).update(**option)
        return instance


def get_total_section_marks(template):
    """Calculate total marks for the template.

    Returns
    -------
    decimal
        Total marks of the sections in the template.

    """
    return sum(section.get_section_marks() for section in template.sections.all())


class SectionCRUDSerializer(serializers.ModelSerializer):
    """CRUD serializer for Section."""

    section_marks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Section
        fields = (
            "id",
            "name",
            "num_of_questions",
            "pos_marks",
            "neg_percentage",
            "template",
            "section_marks",
        )

    def get_section_marks(self, obj):
        return obj.get_section_marks()

    def validate(self, attrs):
        template_instance = self.instance
        template = attrs.get(
            "template", template_instance and template_instance.template
        )
        pos_marks = attrs.get(
            "pos_marks", template_instance and template_instance.pos_marks
        )
        num_of_questions = attrs.get(
            "num_of_questions", template_instance and template_instance.num_of_questions
        )

        template_marks = template.full_marks
        validate_gt_than_template_marks(template_marks, pos_marks)

        section_marks = pos_marks * num_of_questions
        validate_gt_than_template_marks(template_marks, section_marks)

        return attrs


class OptionsOnExamRetrievalSerializer(serializers.ModelSerializer):
    """Serializer for options on exam retrieval."""

    class Meta:
        model = Option
        fields = (
            "id",
            "detail",
            "correct",
            "img",
        )


class QuestionOnExamRetrievalSerializer(serializers.ModelSerializer):
    """Serializer for Question when user is retrieving an exam."""

    options = OptionsOnExamRetrievalSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "detail",
            "img",
            "options",
            "feedback",
            "section",
        )


class SectionOnExamRetrievalSerializer(serializers.ModelSerializer):
    """Serializer for Section on Exam Retrieval."""

    # questions = QuestionOnExamRetrievalSerializer(many=True)

    class Meta:
        model = Section
        fields = (
            "id",
            "name",
            "num_of_questions",
            "pos_marks",
            "neg_percentage",
            # "questions",
        )


class ExamTemplateOnExamRetrievalSerializer(serializers.ModelSerializer):
    """Serializer for ExamTemplate on Exam Retrieval."""

    sections = SectionOnExamRetrievalSerializer(many=True)

    class Meta:
        model = ExamTemplate
        fields = (
            "id",
            "name",
            "full_marks",
            "sections",
            "duration",
        )


class ExamTemplateCreateUpdateSerializer(CreatorSerializer):
    """Exam Template Serializer."""

    pass_marks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExamTemplate
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "description",
            "full_marks",
            "pass_percentage",
            "pass_marks",
            "duration",
            "display_num_questions",
            "status",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    def update(self, instance, validated_data):
        if instance.status == ExamTemplateStatus.COMPLETED:
            raise serializers.ValidationError(
                "Exam Template is already completed. You can not update it."
            )
        full_marks = validated_data.get("full_marks", instance.full_marks)
        status = validated_data.get("status", instance.status)
        total_section_marks = get_total_section_marks(instance)
        print(f"full_marks: {full_marks}, total_section_marks: {total_section_marks}")
        if (status == ExamTemplateStatus.COMPLETED) and (
            full_marks != total_section_marks
        ):
            raise serializers.ValidationError(
                (
                    "Total marks should be equal to sum of section"
                    + " marks on exam completion"
                )
            )
        return super().update(instance, validated_data)

    def get_pass_marks(self, obj):
        return obj.pass_percentage * obj.full_marks


class ExamTemplateRetrieveSerializer(CreatorSerializer):
    """Serializer to retrieve exam template."""

    pass_marks = serializers.SerializerMethodField(read_only=True)
    sections = SectionCRUDSerializer(many=True, read_only=True)
    residual_marks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExamTemplate
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "description",
            "full_marks",
            "pass_percentage",
            "pass_marks",
            "duration",
            "display_num_questions",
            "sections",
            "residual_marks",
            "status",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    def get_pass_marks(self, obj):
        return obj.pass_percentage * obj.full_marks

    def get_residual_marks(self, obj):
        sum_marks = get_total_section_marks(obj)
        return obj.full_marks - sum_marks


class ExamTemplateMiniSerializer(serializers.ModelSerializer):
    """Serializer for ExamTemplateMini."""

    class Meta:
        model = ExamTemplate
        fields = ("id", "name")


class ExamTemplateListAdminSerializer(ExamTemplateListSerializer):
    """Serializer to list exam templates for admin."""

    class Meta:
        model = ExamTemplate
        fields = ExamTemplateListSerializer.Meta.fields


class ExamCreateSerializer(CreatorSerializer):
    """Serializer when admin is creating an exam."""

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


class ExamListAdminSerializer(serializers.ModelSerializer):
    """Serializer when user is listing exams."""

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
    """Serializer when admin is updating an exam."""

    class Meta:
        model = Exam
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "category",
            "status",
            "price",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)


class ExamRetrieveAdminSerializer(serializers.ModelSerializer):
    """Serializer when admin is retrieving an exam."""

    template = ExamTemplateOnExamRetrievalSerializer()
    questions = QuestionOnExamRetrievalSerializer(many=True)
    sessions = SessionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = (
            "id",
            "name",
            "category",
            "status",
            "price",
            "template",
            "sessions",
            "questions",
        )


class ExamImageAdminSerializer(serializers.ModelSerializer):
    """Serializer for Exam Image."""

    url = serializers.SerializerMethodField(read_only=True)
    uploaded = serializers.SerializerMethodField(read_only=True)
    fileName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExamImage
        fields = ("id", "upload", "url", "uploaded", "fileName")

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.upload.url)

    def get_fileName(self, obj):
        return obj.upload.name.split("/")[-1]

    def get_uploaded(self, obj):
        return 1
