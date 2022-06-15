from rest_framework import serializers

from common.api.serializers import CreatorSerializer
from enrollments.api.utils import is_enrolled
from enrollments.models import (
    CourseThroughEnrollment,
    Enrollment,
    EnrollmentStatus,
    ExamEnrollmentStatus,
    ExamThroughEnrollment,
    PhysicalBookCourseEnrollment,
    QuestionEnrollment,
    Session,
)
from exams.models import Exam, Option, Question


class SessionSerializer(CreatorSerializer):
    """Serializer for Session model."""

    class Meta:
        model = Session
        fields = CreatorSerializer.Meta.fields + (
            "start_date",
            "end_date",
            "status",
            "exam",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + ("status",)


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


class PhysicalBookCourseEnrollmentSerializer(serializers.ModelSerializer):
    """Physical book when user enrolls to course."""

    class Meta:
        model = PhysicalBookCourseEnrollment
        fields = (
            "physical_book",
            "course_enrollment",
            "status_provided",
        )


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    """Course when the user is enrolled."""

    physical_books = PhysicalBookCourseEnrollmentSerializer(many=True)

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "course",
            "enrollement",
            "selected_session",
            "course_status",
            "joining_date",
            "completed_date",
            "physical_books",
        )


class CourseEnrollmentUpdateSerializer(serializers.ModelSerializer):
    """Course Update serializer after the user is enrolled."""

    physical_books = PhysicalBookCourseEnrollmentSerializer(many=True)

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "course",
            "enrollement",
            "selected_session",
            "course_status",
            "joining_date",
            "completed_date",
            "physical_books",
        )


class CourseEnrollmentRetrieveSerializer(serializers.ModelSerializer):
    """Serializer when the user is retrieving an enrollment."""

    physical_books = PhysicalBookCourseEnrollmentSerializer(many=True)

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "course",
            "enrollement",
            "selected_session",
            "course_status",
            "joining_date",
            "completed_date",
            "physical_books",
        )


class EnrollmentRetrieveSerializer(serializers.ModelSerializer):
    """Serializer when user is retrieving an enrollment."""

    exams = ExamEnrollmentSerializer(many=True, source="exam_enrolls")
    courses = CourseEnrollmentSerializer(many=True)

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


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    """Serializer when user is enrolling into an exam.

    It handles the enrollment creation either for exam or course or  both.
    """

    exams = ExamEnrollmentSerializer(many=True, source="exam_enrolls", required=False)
    courses = CourseEnrollmentSerializer(many=True)

    class Meta:
        model = Enrollment
        fields = (
            "id",
            # 'student',
            "exams",
            "courses",
        )

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
        user = self.context["request"].user
        total_price = 0.0
        if not (exams_data):
            raise serializers.ValidationError("Atleast one fields should be non-empty.")

        def batch_is_enrolled_and_price(enrolled_objs):
            sum_price = 0.0
            for enrolled_obj in enrolled_objs:
                sum_price += float(enrolled_obj.price)
                # if he_is_enrolled := is_enrolled(enrolled_obj, user):
                if is_enrolled(enrolled_obj, user):
                    raise serializers.ValidationError(
                        f"{user} is already enrolled into {enrolled_obj}"
                    )
            return sum_price

        # if parts:
        #     total_price += batch_is_enrolled_and_price(parts)
        # if notes:
        #     total_price += batch_is_enrolled_and_price(notes)
        if exams_data:
            exams = [data.get("exam") for data in exams_data]
            total_price += batch_is_enrolled_and_price(exams)
        enrollment = super().create(validated_data)

        if exams_data:
            for data in exams_data:
                exam = data.get("exam")
                selected_session = data.get("selected_session")
                ExamThroughEnrollment(
                    enrollment=enrollment, exam=exam, selected_session=selected_session
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
            "rank",
            "status",
        )

    def get_rank(self, obj):
        """Get the rank of the user in the exam.

        This is based on the score of current exam takers.

        Parameters
        ----------
        obj : ExamThroughEnrollment
            exam enrollment.

        Returns
        -------
        int
            rank of the user in the exam.

        """
        all_examinee_states = ExamThroughEnrollment.objects.filter(exam=obj.exam)
        num_examinee = all_examinee_states.count()
        num_examinee_lower_score = all_examinee_states.filter(
            score__lt=obj.score
        ).count()
        return num_examinee - num_examinee_lower_score

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

    selected_session = SessionSerializer()

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "selected_session",
            "exam",
        )
