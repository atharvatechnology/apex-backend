from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from accounts.api_admin.serializers import UserMiniAdminSerializer
from common.api.serializers import CreatorSerializer, DynamicFieldsCategorySerializer
from common.utils import decode_user
from courses.api_common.serializers import CoursePhysicalSerializer
from courses.models import Course, CourseStatus
from enrollments.api.serializers import ExamEnrollmentSerializer
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
)
from exams.api_common.serializers import ExamMiniSerializer
from payments.api_common.serializers import PaymentSerializer
from physicalbook.api_admin.serializers import PhysicalBookAdminListSerializer

User = get_user_model()


class ExamSessionAdminSerializer(
    DynamicFieldsCategorySerializer,
    CreatorSerializer,
):
    """Serializer for Session create."""

    # name = serializers.CharField(max_length=255, read_only=True)

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

    # def validate(self, data):
    #     """Filter based on ExamSession and check if obj exists."""
    #     obj = self.Meta.model.objects.filter(exam=data["exam"])

    #     if obj.exists():
    #         raise serializers.ValidationError("Exam cannot be more than one session.")

    #     return data

    @transaction.atomic
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


class ExamSessionAdminUpdateSerializer(ExamSessionAdminSerializer):
    """Serializer for Session update."""

    class Meta:
        model = ExamSession
        fields = ExamSessionAdminSerializer.Meta.fields
        read_only_fields = ExamSessionAdminSerializer.Meta.read_only_fields + (
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


class CourseSessionAdminSerializer(CreatorSerializer):
    """Serializer for Session Create."""

    class Meta:
        model = CourseSession
        fields = CreatorSerializer.Meta.fields + (
            "start_date",
            "end_date",
            "status",
            "course",
            "name",
        )
        read_only_fields = CreatorSerializer.Meta.read_only_fields + (
            "status",
            "end_date",
        )

        def create(self, validated_data):
            """Create a new session."""
            try:
                instance = super().create(validated_data)
                instance.full_clean()
            except ValidationError as error:
                raise serializers.ValidationError(
                    serializers.as_serializer_error(error)
                ) from error
            return instance


class CourseSessionAdminUpdateSerializer(CourseSessionAdminSerializer):
    """Serializer for course session update."""

    class Meta:
        model = CourseSession
        fields = CourseSessionAdminSerializer.Meta.fields
        read_only_fields = CourseSessionAdminSerializer.Meta.read_only_fields + (
            "start_date",
            "end_date",
        )

    def update(self, instance, validated_data):
        """Update an existing Session."""
        try:
            instance = super().update(instance, validated_data)
            instance.full_clean()
        except ValidationError as error:
            raise serializers.ValidationError(
                serializers.as_serializer_error(error)
            ) from error
        return instance


class EnrollmentStatusAdminUpdateSerializer(serializers.ModelSerializer):
    """Serializer for enrollment status update."""

    class Meta:
        model = Enrollment
        fields = ("status",)


class ExamThroughEnrollmentAdminBaseSerializer(serializers.ModelSerializer):
    """Base Serializer for ExamThroughEnrollment."""

    exam = ExamMiniSerializer()
    student = UserMiniAdminSerializer(source="enrollment.student")
    selected_session = ExamSessionAdminSerializer()
    created_at = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    enrollment_id = serializers.SerializerMethodField()

    class Meta:
        model = ExamThroughEnrollment
        fields = (
            "id",
            "selected_session",
            "student",
            "status",
            "score",
            "negative_score",
            "exam",
            "payment",
            "created_at",
            "enrollment_id",
        )
        read_only_fields = (
            "status",
            "score",
        )

    def get_created_at(self, obj):
        """Get created_at."""
        return obj.enrollment.created_at

    def get_payment(self, obj):
        """Get payment."""
        data = PaymentSerializer(
            obj.enrollment.payments_payment_related.all(), many=True
        ).data
        return data

    def get_status(self, obj):
        """Get enrollment status."""
        return obj.status

    def get_enrollment_id(self, obj):
        return obj.enrollment.id


class ExamThroughEnrollmentAdminListSerializer(
    ExamThroughEnrollmentAdminBaseSerializer
):
    """Serializer for ExamThroughEnrollment List."""

    question_states = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    enrollment_status = serializers.SerializerMethodField()

    class Meta:
        model = ExamThroughEnrollment
        fields = ExamThroughEnrollmentAdminBaseSerializer.Meta.fields + (
            "question_states",
            "rank",
            "enrollment",
            "enrollment_status",
        )

    def get_rank(self, obj):
        return get_student_rank(obj)

    def get_enrollment_status(self, obj):
        return obj.enrollment.status

    # @staticmethod
    # def get_student(obj):
    #     return obj.enrollment.student.__str__()

    @staticmethod
    def get_question_states(obj):
        return obj.question_states.all().count()


class PhysicalBookCourseEnrollmentAdminSerializer(serializers.ModelSerializer):
    """Serializer for Admin for Physical book when user enrolls to course."""

    physical_book = PhysicalBookAdminListSerializer()

    class Meta:
        model = PhysicalBookCourseEnrollment
        fields = (
            "id",
            "physical_book",
            "course_enrollment",
            "status_provided",
        )


class PhysicalBookCourseEnrollmentCreateAdminSerializer(serializers.ModelSerializer):
    """Serializer for Creating Admin Physical Book."""

    class Meta:
        model = PhysicalBookCourseEnrollment
        fields = (
            "id",
            "physical_book",
            "course_enrollment",
            "status_provided",
        )

    def create(self, validated_data):
        physical_book = validated_data.get("physical_book")
        course_through_enrollment = validated_data.get("course_enrollment")
        course = course_through_enrollment.course

        physical_course = physical_book.course

        if physical_course == course:
            return super().create(validated_data)
        else:

            raise serializers.ValidationError("Course has no PhysicalBook.")


class PhysicalBookCourseEnrollmentUpdateAdminSerializer(serializers.ModelSerializer):
    """Serializer for updating for Physical Book."""

    class Meta:
        model = PhysicalBookCourseEnrollment
        fields = (
            "id",
            "physical_book",
            "course_enrollment",
            "status_provided",
        )


class CourseThroughEnrollmentAdminBaseSerializer(serializers.ModelSerializer):
    """Base Serializer for CourseThroughEnrollment."""

    course = CoursePhysicalSerializer()
    student = UserMiniAdminSerializer(source="enrollment.student")
    selected_session = CourseSessionAdminSerializer()
    created_at = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    physicalbook_enrolls = PhysicalBookCourseEnrollmentAdminSerializer(many=True)
    enrollment_id = serializers.SerializerMethodField()

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "selected_session",
            "student",
            "course",
            "payment",
            "created_at",
            "status",
            "enrollment",
            "physicalbook_enrolls",
            "enrollment_id",
        )
        read_only_fields = ("status",)

    def get_status(self, obj):
        """Get enrollment status."""
        return obj.enrollment.status

    def get_created_at(self, obj):
        """Get created_at."""
        return obj.enrollment.created_at

    def get_payment(self, obj):
        """Get payment."""
        return PaymentSerializer(
            obj.enrollment.payments_payment_related.all(), many=True
        ).data

    def get_enrollment_id(self, obj):
        return obj.enrollment.id


class CourseThroughEnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for CourseThroughEnrollment."""

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "selected_session",
            "course",
            "course_enroll_status",
        )
        read_only_fields = (
            "course_enroll_status",
            "id",
        )


class CourseEnrollmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating enrollments into a course."""

    courses = CourseThroughEnrollmentSerializer(many=True, source="course_enrolls")

    class Meta:
        model = Enrollment
        fields = (
            "courses",
            "student",
            "status",
        )
        read_only_fields = ("status",)

    @transaction.atomic
    def create(self, validated_data):
        """Create a new enrollment of student to the course."""
        courses_data = validated_data.pop("course_enrolls", None)
        student_user = validated_data.get("student")
        total_price = 0.0
        courses = [data.get("course") for data in courses_data]
        total_price += batch_is_enrolled_and_price(courses, student_user)
        enrollment = super().create(validated_data)
        for data in courses_data:
            course = data.get("course")
            session = data.get("selected_session")
            CourseThroughEnrollment(
                course=course, enrollment=enrollment, selected_session=session
            ).save()
        enrollment.status = EnrollmentStatus.ACTIVE
        enrollment.save()
        return enrollment


class ExamEnrollmentCreateSerializer(serializers.ModelSerializer):
    exams = ExamEnrollmentSerializer(many=True, source="exam_enrolls")

    class Meta:
        model = Enrollment
        fields = (
            "student",
            "exams",
        )

    def create(self, validated_data):
        exams_data = validated_data.pop("exam_enrolls", None)
        user = validated_data.get("student")

        exams = [data.get("exam") for data in exams_data]
        batch_is_enrolled_and_price(exams, user)
        enrollment = super().create(validated_data)

        exam_data_save(exams_data, enrollment)
        enrollment.status = EnrollmentStatus.ACTIVE
        enrollment.save()
        return enrollment


class StudentEnrollmentCheckSerializer(serializers.Serializer):
    """Student Enrollment check against course."""

    user = serializers.CharField()
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    def validate_user(self, value):
        decoded_username = decode_user(value)
        if decoded_username is not None:
            user = User.objects.filter(username=decoded_username).first()
            enrolled_student = (
                CourseThroughEnrollment.objects.filter(
                    enrollment__student=user, course__status=CourseStatus.INSESSION
                )
                or None
            )
            if enrolled_student is not None:
                return user
            else:
                raise serializers.ValidationError(
                    "Student is not enrolled in any course."
                )
        raise serializers.ValidationError("Invalid user")

    def validate(self, attrs):
        user = attrs.get("user")
        course = attrs.get("course")
        enrolled_student = (
            CourseThroughEnrollment.objects.filter(
                enrollment__student=user,
                course=course,
                course__status=CourseStatus.INSESSION,
            )
            or None
        )
        if enrolled_student is not None:
            return super().validate(attrs)
        raise serializers.ValidationError(f"Student is not enrolled in {course}.")


class ExamSessionListSerializer(serializers.ModelSerializer):

    examinee = serializers.SerializerMethodField(read_only=True)
    passed = serializers.SerializerMethodField(read_only=True)
    start_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExamSession
        fields = (
            "name",
            "start_date",
            "status",
            "examinee",
            "passed",
            # "failed",
        )

    def get_start_date(self, obj):
        return obj.start_date.strftime("%d %b %Y")

    def get_examinee(self, obj):
        return obj.session_enrolls.all().count()

    def get_passed(self, obj):
        return obj.session_enrolls.filter(status=ExamEnrollmentStatus.PASSED).count()
