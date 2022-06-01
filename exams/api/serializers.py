from rest_framework import serializers

from common.api.mixin import EnrolledSerializerMixin
from common.api.serializers import CreatorSerializer
from enrollments.api.serializers import ExamEnrollmentPaperSerializer, SessionSerializer
from enrollments.models import ExamEnrollmentStatus
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


class ExamRetrieveSerializer(CreatorSerializer, EnrolledSerializerMixin):
    template = ExamTemplateSerializer()
    sessions = SessionSerializer(many=True)
    has_submitted = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "category",
            "status",
            "price",
            "is_enrolled",
            "is_enrolled_active",
            "sessions",
            "template",
            "has_submitted",
        )

    def get_has_submitted(self, obj):
        enrollments = []
        user = self.context["request"].user
        if user.is_authenticated:
            enrollments = obj.enrolls.all().filter(student=user)
        if len(enrollments) > 0:
            enrollment = enrollments.first()
            exam_enrollment = enrollment.exam_enrolls.all().filter(exam=obj).first()
            if exam_enrollment.status != ExamEnrollmentStatus.CREATED:
                return True
        return False


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
    exam_enroll = serializers.SerializerMethodField()

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
            "exam_enroll",
        )

    def get_exam_enroll(self, obj):
        if self.context["request"].user.is_authenticated:
            student_enrollments = obj.enrolls.filter(
                student=self.context["request"].user
            )
            if student_enrollments.count() > 0:
                return ExamEnrollmentPaperSerializer(
                    student_enrollments[0].exam_enrolls.filter(exam=obj).first()
                ).data


# class ExamPaperWOEnrollmentSeriaizer(serializers.ModelSerializer):
#     template = ExamTemplateSerializer()
#     questions = QuestionSerializer(many=True)

#     class Meta:
#         model = Exam
#         fields = (
#             "id",
#             "name",
#             "category",
#             "status",
#             "price",
#             "questions",
#             "template",
#         )
