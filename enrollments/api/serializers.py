from django.db import transaction
from rest_framework import serializers
from rest_framework.response import Response

from common.api.serializers import CreatorSerializer
from common.utils import decode_user
from courses.models import Course
from enrollments.api.utils import (
    batch_is_enrolled_and_price,
    exam_data_save,
    get_student_rank,
)
from enrollments.models import (
    CourseSession,
    CourseThroughEnrollment,
    Enrollment,
    EnrollmentStatus,
    ExamEnrollmentStatus,
    ExamSession,
    ExamThroughEnrollment,
    PhysicalBookCourseEnrollment,
    QuestionEnrollment,
    Session,
)
from exams.models import Exam, ExamTemplate, Option, Question
from meetings.api.serializers import MeetingOnCourseEnrolledSerializer


class SessionSerializer(CreatorSerializer):
    """Serializer for Session model."""

    class Meta:
        model = Session
        fields = CreatorSerializer.Meta.fields + (
            "start_date",
            "end_date",
            "status",
            "name",
            # "exam",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)


class ExamSessionSerializer(SessionSerializer):
    """Serializer for ExamSession model."""

    class Meta:
        model = ExamSession
        fields = SessionSerializer.Meta.fields + ("exam",)
        read_only_fields = SessionSerializer.Meta.read_only_fields


class CourseSessionSerializer(SessionSerializer):
    class Meta:
        model = CourseSession
        fields = SessionSerializer.Meta.fields + ("course",)


class SelectedCourseSessionSerializer(SessionSerializer):
    """Serializer for retrieving selected course session after enrollment."""

    meetings = MeetingOnCourseEnrolledSerializer(many=True)

    class Meta:
        model = CourseSession
        fields = SessionSerializer.Meta.fields + (
            "course",
            "meetings",
        )


class TemplateSerializer(CreatorSerializer):
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


class ExamInfoSerializer(serializers.ModelSerializer):
    """Serializer for Exam Info."""

    template = TemplateSerializer()

    class Meta:
        model = Exam
        fields = (
            "id",
            "name",
            "category",
            "price",
            "template",
        )


class ExamEnrollmentSerializer(serializers.ModelSerializer):
    """Serializer when user enrolls to an exam.

    This is also used when user retrieves their exam enrollment.
    """

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "exam",
            "selected_session",
        )


# new changes
class ExamEnrollmentListSerializer(serializers.ModelSerializer):
    """Serializer when user enrolls to an exam.

    This is also used when user retrieves their exam enrollment.
    """

    exam = ExamInfoSerializer()
    start_date = serializers.SerializerMethodField()

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "exam",
            "start_date",
            "selected_session",
        )

    def get_start_date(self, obj):
        return obj.selected_session.start_date


# -------------
class PhysicalBookCourseEnrollmentSerializer(serializers.ModelSerializer):
    """Physical book when user enrolls to course."""

    class Meta:
        model = PhysicalBookCourseEnrollment
        fields = (
            "physical_book",
            "course_enrollment",
            "status_provided",
        )


class CourseInfoSerializer(serializers.ModelSerializer):
    enrollment_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "category",
            "description",
            "link",
            "password",
            "status",
            "price",
            "duration",
            "image",
            "enrollment_count",
        )

    def get_enrollment_count(self, obj):
        return {"course_enroll_count": obj.course_enrolls.all().count()}


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    """Course when the user is enrolled."""

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "course",
            "selected_session",
            "completed_date",
        )


# new changes
class CourseEnrollmentListSerializer(serializers.ModelSerializer):
    """Course when the user is enrolled."""

    course = CourseInfoSerializer()

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "course",
            "selected_session",
            "completed_date",
        )


# ------------------


class CourseEnrollmentUpdateSerializer(serializers.ModelSerializer):
    """Course Update serializer after the user is enrolled."""

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "course",
            "enrollment",
            "selected_session",
            "course_enroll_status",
            "completed_date",
        )


class CourseEnrollmentRetrieveSerializer(serializers.ModelSerializer):
    """Serializer when the user is retrieving an enrollment."""

    physical_books = PhysicalBookCourseEnrollmentSerializer(many=True)

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "course",
            "enrollment",
            "selected_session",
            "course_enroll_status",
            "completed_date",
            "physical_books",
        )


# class EnrollmentRetrieveSerializer(serializers.ModelSerializer):
#     """Serializer when user is retrieving an enrollment."""

#     exams = ExamEnrollmentSerializer(many=True, source="exam_enrolls")
#     courses = CourseEnrollmentSerializer(many=True, source="course_enrolls")

#     class Meta:
#         model = Enrollment
#         fields = (
#             "id",
#             "student",
#             "status",
#             "exams",
#             "courses",
#         )
#         read_only_fields = ("status",)


# new changes


class EnrollmentRetrieveSerializer(serializers.ModelSerializer):
    """Serializer when user is retrieving an enrollment."""

    exams = ExamEnrollmentListSerializer(many=True, source="exam_enrolls")
    courses = CourseEnrollmentListSerializer(many=True, source="course_enrolls")

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "student",
            "status",
            "exams",
            "courses",
        )
        read_only_fields = ("status",)


# new change


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    """Serializer when user is enrolling into an exam.

    It handles the enrollment creation either for exam or course or  both.
    """

    exams = ExamEnrollmentSerializer(many=True, source="exam_enrolls", required=False)
    courses = CourseEnrollmentSerializer(
        many=True, source="course_enrolls", required=False
    )

    class Meta:
        model = Enrollment
        fields = (
            "id",
            # 'student',
            "exams",
            "courses",
        )

    @transaction.atomic
    def create(self, validated_data):
        """Create an enrollment.

        Parameters
        ----------
        validated_data : dict
            validated enrollment data.

        Returns
        -------
        Enrollment
            created enrollment.

        Raises
        ------
        serializers.ValidationError
            if the user is already enrolled.
        serializers.ValidationError
            other validation error

        """

        exams_data = validated_data.pop("exam_enrolls", None)
        courses_data = validated_data.pop("course_enrolls", None)
        user = self.context["request"].user
        total_price = 0.0
        if not (exams_data or courses_data):
            raise serializers.ValidationError("Atleast one fields should be non-empty.")
        # if parts:
        #     total_price += batch_is_enrolled_and_price(parts)
        # if notes:
        #     total_price += batch_is_enrolled_and_price(notes)
        if exams_data:
            exams = [data.get("exam") for data in exams_data]
            total_price += batch_is_enrolled_and_price(exams, user)
        enrollment = super().create(validated_data)

        exam_data_save(exams_data, enrollment)
        if courses_data:
            courses_all = [data.get("course") for data in courses_data]
            total_price += batch_is_enrolled_and_price(courses_all, user)
            for data in courses_data:
                course = data.get("course")
                selected_session = data.get("selected_session")
                completed_date = data.get("completed_date")
                student = enrollment.student
                course_enrollment = CourseThroughEnrollment.objects.filter(
                    course=course, enrollment__student=student
                )
                if course_enrollment:
                    raise serializers.ValidationError(
                        "User is already enrolled to the course"
                    )
                CourseThroughEnrollment(
                    course=course,
                    enrollment=enrollment,
                    selected_session=selected_session,
                    completed_date=completed_date,
                ).save()
        if total_price == 0.0:
            enrollment.status = EnrollmentStatus.ACTIVE
        enrollment.save()
        return enrollment


class OptionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            "id",
            "detail",
            "correct",
            "img",
        )


class QuestionResultSerializer(serializers.ModelSerializer):
    options = OptionResultSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "detail",
            "img",
            "feedback",
            "options",
        )


class QuestionEnrollmentSerializer(serializers.ModelSerializer):
    """Serializer when user retrieves his latest exam result."""

    # question = serializers.SerializerMethodField()

    class Meta:
        model = QuestionEnrollment
        fields = (
            "id",
            "question",
            "selected_option",
        )

    # def get_question(self, obj):
    #     """Get question result."""
    #     return QuestionResultSerializer(obj.question).data


class QuestionEnrollmentSubmitSerializer(serializers.ModelSerializer):
    """Serializer when user submits his exam's question answers."""

    class Meta:
        model = QuestionEnrollment
        fields = (
            "id",
            "question",
            "selected_option",
        )


class ExamEnrollmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer when user submits his exam.

    This is also to partially submit his exam i.e save the result of the exam.
    When user fully submits his exam,
    the status of the enrollment is changed to ATTEMPTED.
    """

    question_states = QuestionEnrollmentSubmitSerializer(many=True)
    submitted = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "question_states",
            "status",
            "submitted",
        )
        read_only_fields = ("status",)

    def update(self, instance, validated_data):
        """Update an exam enrollment.

        Parameters
        ----------
        instance : ExamThroughEnrollment
            exam enrollment to be updated.
        validated_data : dict
            validated data.

        Returns
        -------
        ExamThroughEnrollment
            updated exam enrollment.

        """
        question_states = validated_data.pop("question_states")
        submitted = validated_data.get("submitted") or False

        for state_data in question_states:
            question = state_data.get("question")
            option = state_data.get("selected_option")
            prev_question_states = instance.question_states.all()
            prev_states = prev_question_states.filter(question=question)
            if len(prev_states) > 0:
                prev_state = prev_states.first()
                prev_state.question = question
                prev_state.selected_option = option
                prev_state.save()
            else:
                new_state = QuestionEnrollment(
                    exam_stat=instance, question=question, selected_option=option
                )
                new_state.save()
        if submitted:
            if instance.status == ExamEnrollmentStatus.CREATED:
                instance.attempt_exam()
        else:
            instance.save()
        return instance


class ExamNameSerializer(serializers.ModelSerializer):
    """Serializer for exam name."""

    questions = QuestionResultSerializer(many=True)

    class Meta:
        model = Exam
        fields = (
            "id",
            "name",
            "questions",
        )


class ExamEnrollmentRetrieveSerializer(serializers.ModelSerializer):
    """Serializer when user retrieves his latest exam result."""

    question_states = QuestionEnrollmentSerializer(many=True)
    rank = serializers.SerializerMethodField()
    exam = ExamNameSerializer()

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "enrollment",
            "exam",
            "question_states",
            "score",
            "negative_score",
            "rank",
            "status",
        )

    def get_rank(self, obj):
        return get_student_rank(obj)

    # def get_exam(self):
    #     from exams.api.serializers import ExamPaperWOEnrollmentSeriaizer
    #     return ExamPaperWOEnrollmentSeriaizer(self.exam).data


class ExamEnrollmentRetrievePoolSerializer(serializers.ModelSerializer):
    """Serializer when user retrieves his latest exam result with pooling."""

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "status",
        )


class ExamEnrollmentCheckPointRetrieveSerializer(serializers.ModelSerializer):
    """Serializer when user retrieves his latest exam result."""

    question_states = QuestionEnrollmentSerializer(many=True)
    # exam = ExamNameSerializer()

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "enrollment",
            "exam",
            "question_states",
            "status",
        )

    # def get_exam(self):
    #     from exams.api.serializers import ExamPaperWOEnrollmentSeriaizer
    #     return ExamPaperWOEnrollmentSeriaizer(self.exam).data


class ExamEnrollmentPaperSerializer(serializers.ModelSerializer):
    """Serializer when user retrieves his latest exam schedule."""

    selected_session = ExamSessionSerializer()

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "selected_session",
            "exam",
        )


class StudentEnrollmentSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    course = serializers.IntegerField()
    session = serializers.IntegerField()

    def validate(self, data):
        usr_name = data["username"]
        course_id = data["course"]
        session_id = data["session"]
        decoded_data = decode_user(usr_name)

        queryset = (
            CourseThroughEnrollment.objects.filter(
                enrollment__student__username=decoded_data,
                course__id=course_id,
                selected_session__id=session_id,
            )
            or None
        )
        if queryset is None:
            raise serializers.ValidationError({"msg": "Enrollment Required."})
        return Response({"msg": "You are enrolled."})
