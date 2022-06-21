from rest_framework import serializers

from common.api.mixin import EnrolledSerializerMixin
from common.api.serializers import CreatorSerializer
from enrollments.api.serializers import ExamEnrollmentPaperSerializer, SessionSerializer
from enrollments.models import ExamEnrollmentStatus, ExamThroughEnrollment
from exams.models import Exam, ExamTemplate, Option, Question, Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = (
            "id",
            "name",
            "num_of_questions",
            "pos_marks",
            "neg_percentage",
            "template",
        )


class ExamTemplateSerializer(CreatorSerializer):
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
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    def get_pass_marks(self, obj):
        return obj.pass_percentage * obj.full_marks


class ExamTemplateRetrieveSerializer(CreatorSerializer):
    """Serializer to retrieve exam template."""

    pass_marks = serializers.SerializerMethodField(read_only=True)
    sections = SectionSerializer(many=True, read_only=True)

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
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    def get_pass_marks(self, obj):
        return obj.pass_percentage * obj.full_marks


class ExamTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTemplate
        fields = (
            "id",
            "name",
            "description",
            "duration",
            "full_marks",
            "pass_percentage",
            "display_num_questions",
        )


class ExamEnrollmentExamRetrieveSerializer(serializers.ModelSerializer):
    """Serializer of ExamEnroll when user is retrieving an exam."""

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "status",
        )


class ExamRetrieveSerializer(CreatorSerializer, EnrolledSerializerMixin):
    """Serializer when user is retrieving an exam."""

    template = ExamTemplateSerializer()
    sessions = SessionSerializer(many=True)
    exam_enroll = serializers.SerializerMethodField()

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
            "exam_enroll",
        )

    def get_exam_enroll(self, obj):
        """Retrieve exam enroll of current user.

        If user is not enrolled, return None.

        Parameters
        ----------
        obj : Exam
            instance of Exam db object.

        Returns
        -------
        ExamThroughEnrollment
            instance of ExamThroughEnrollment db object.

        """
        enrollments = []
        user = self.context["request"].user
        if user.is_authenticated:
            enrollments = obj.enrolls.all().filter(student=user)
        if len(enrollments) > 0:
            enrollment = enrollments.first()
            exam_enrollment = enrollment.exam_enrolls.all().filter(exam=obj).first()
            if exam_enrollment.status != ExamEnrollmentStatus.CREATED:
                return ExamEnrollmentExamRetrieveSerializer(exam_enrollment).data
        return None


class ExamRetrievePoolSerializer(serializers.ModelSerializer):
    """Serializer when user is retrieving an exam for pooling."""

    class Meta:
        model = Exam
        fields = (
            "id",
            "status",
        )


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


class ExamListSerializer(serializers.ModelSerializer):
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
