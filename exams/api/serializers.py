from rest_framework import serializers

from common.api.mixin import EnrolledSerializerMixin
from common.api.serializers import CreatorSerializer
from enrollments.api.serializers import (
    ExamEnrollmentPaperSerializer,
    ExamSessionSerializer,
)
from enrollments.api.utils import retrieve_exam_status
from enrollments.models import (
    Enrollment,
    EnrollmentStatus,
    ExamEnrollmentStatus,
    ExamThroughEnrollment,
    SessionStatus,
)
from exams.models import Exam, ExamTemplate, ExamType, Option, Question


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
            # "status",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    # def update(self, instance, validated_data):
    #     full_marks = validated_data.get("full_marks", instance.full_marks)
    #     status = validated_data.get("status", instance.status)
    #     total_section_marks = get_total_section_marks(instance)
    #     print(f"full_marks: {full_marks}, total_section_marks: {total_section_marks}")
    #     if (status == ExamTemplateStatus.COMPLETED) and (
    #         full_marks != total_section_marks
    #     ):
    #         raise serializers.ValidationError(
    #             (
    #                 "Total marks should be equal to sum of section"
    #                 + " marks on exam completion"
    #             )
    #         )
    #     return super().update(instance, validated_data)

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
    sessions = ExamSessionSerializer(many=True)
    exam_enroll = serializers.SerializerMethodField()
    session_id = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    active_exam_is_submitted = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "exam_type",
            "category",
            "status",
            "price",
            "is_enrolled",
            "is_enrolled_active",
            "sessions",
            "template",
            "exam_enroll",
            "session_id",
            "active_exam_is_submitted",
        )

    def _get_cached_enrollments(self, obj, user):
        if not hasattr(self, "_cached_enrollments"):
            enrollments = list(obj.enrolls.all().filter(student=user).order_by("-id"))
            self._cached_enrollments = enrollments
            return enrollments
        return self._cached_enrollments

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
            enrollments = self._get_cached_enrollments(obj, user)
        if len(enrollments) > 0:
            enrollment = enrollments[0]
            if enrollment.status != EnrollmentStatus.ACTIVE:
                return None
            exam_enrollment = (
                enrollment.exam_enrolls.all().filter(exam=obj).latest("id")
            )
            if exam_enrollment.status != ExamEnrollmentStatus.CREATED:
                return ExamEnrollmentExamRetrieveSerializer(exam_enrollment).data
        return None

    def get_active_exam_is_submitted(self, obj):
        if obj.exam_type != ExamType.PRACTICE:
            return None
        enrollments = []
        user = self.context["request"].user
        if user.is_authenticated:
            enrollments = self._get_cached_enrollments(obj, user)
        if len(enrollments) > 0:
            enrollment = enrollments[0]
            exam_enrollment = (
                enrollment.exam_enrolls.all().filter(exam=obj).latest("id")
            )
            sel_sess = exam_enrollment.selected_session
            if sel_sess.status == SessionStatus.ACTIVE and exam_enrollment.status in [
                ExamEnrollmentStatus.PASSED,
                ExamEnrollmentStatus.FAILED,
            ]:
                return True
        return False

    def get_session_id(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return None
        enrollments = ExamThroughEnrollment.objects.filter(
            enrollment__student=self.context["request"].user,
            exam=obj,
        )
        if enrollments:
            for exam_enrollment in enrollments:
                if exam_enrollment.selected_session.status in [
                    SessionStatus.ACTIVE,
                    SessionStatus.INACTIVE,
                ]:
                    return exam_enrollment.selected_session.id
        return None

    def get_status(self, obj):
        return retrieve_exam_status(self, obj)


class ExamRetrievePoolSerializer(serializers.ModelSerializer):
    """Serializer when user is retrieving an exam for pooling."""

    # status = serializers.SerializerMethodField()
    class Meta:
        model = Exam
        fields = (
            "id",
            # "status",
        )

    # def get_status(self, obj):
    #     return


class ExamCreateSerializer(CreatorSerializer):
    """Serializer when admin is creating an exam."""

    status = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "category",
            "status",
            "price",
            "template",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    # TODO Need to be discussed.
    def get_status(self, obj):
        return retrieve_exam_status(self, obj)


class ExamListSerializer(serializers.ModelSerializer):
    """Serializer when user is listing exams."""

    template = ExamTemplateListSerializer()
    #status = serializers.SerializerMethodField()
    session = serializers.SerializerMethodField()
    question_count = serializers.SerializerMethodField()

    @staticmethod
    def setup_eager_loading(queryset):
        """Perform necessary eager loading of data."""
        queryset = queryset.prefetch_related("sessions", "category", "questions")
        queryset = queryset.select_related("template")
        # queryset = queryset.annotate(question_count=Count("questions"))
        return queryset

    class Meta:
        model = Exam
        fields = (
            "id",
            "name",
            "exam_type",
            "category",
            #"status",
            "price",
            "template",
            "session",
            "question_count",
        )

    def get_status(self, obj):
        return retrieve_exam_status(self, obj)

    def get_session(self, obj):
        sessions = obj.sessions.all()
        if sessions.count() > 1:
            return "Multiple"
        elif sessions.count() == 0:
            return "No session"
        else:
            return sessions[0].start_date

    def get_question_count(self, obj):
        return obj.questions.count()


class ExamUpdateSerializer(CreatorSerializer):
    """Serializer when admin is updating an exam."""

    status = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = CreatorSerializer.Meta.fields + (
            "name",
            "category",
            "status",
            "price",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields

    def get_status(self, obj):
        return retrieve_exam_status(self, obj)


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
    status = serializers.SerializerMethodField()

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

    def _get_student_enrollment(self, obj):
        if not hasattr(self, "_student_enrollment"):
            try:
                student_enrollment = obj.enrolls.filter(
                    student=self.context["request"].user
                ).latest("id")
            except Enrollment.DoesNotExist:
                student_enrollment = None
            self._student_enrollment = student_enrollment
        return self._student_enrollment

    def get_exam_enroll(self, obj):
        if self.context["request"].user.is_authenticated:
            if hasattr(self.context["request"], "student_enrollment"):
                student_enrollment = self.context["request"].student_enrollment
            else:
                # try:
                #     student_enrollment = obj.enrolls.filter(
                #         student=self.context["request"].user
                #     ).latest("id")
                # except:
                #     student_enrollment = None
                student_enrollment = self._get_student_enrollment(obj)
            if student_enrollment:
                if hasattr(self.context["request"], "student_through_enrollment"):
                    student_through_enrollment = self.context[
                        "request"
                    ].student_through_enrollment
                else:
                    student_through_enrollment = (
                        student_enrollment.exam_enrolls.filter(exam=obj)
                        .select_related("selected_session")
                        .latest("id")
                    )
                return ExamEnrollmentPaperSerializer(
                    student_through_enrollment
                    # student_enrollment.exam_enrolls.filter(exam=obj).latest("id")
                ).data

    def get_status(self, obj):
        return retrieve_exam_status(self, obj)


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
