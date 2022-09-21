from rest_framework import serializers

from common.api.mixin import EnrolledSerializerMixin
from courses.models import Course, CourseCategory
from enrollments.api.serializers import (
    CourseSessionSerializer,
    SelectedCourseSessionSerializer,
)
from enrollments.models import CourseEnrollmentStatus, CourseThroughEnrollment
from notes.api.serializers import (
    NoteSerializerAfterEnroll,
    RecordedVideoDetailSerializer,
)
from physicalbook.api.serializers import PhysicalBookSerializerBeforeEnroll


class CourseEnrollmentCourseRetrieveSerializer(serializers.ModelSerializer):
    """Serializer of ExamEnroll when user is retrieving an exam."""

    selected_session = SelectedCourseSessionSerializer()

    class Meta:
        model = CourseThroughEnrollment
        fields = (
            "id",
            "course_enroll_status",
            "selected_session",
        )


class CourseListSerializer(serializers.ModelSerializer):
    """serializer when user is listing course."""

    enrollment_count = serializers.SerializerMethodField()
    sessions = CourseSessionSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "name", "enrollment_count", "image", "sessions"]

    @staticmethod
    def get_enrollment_count(obj):
        return {"course_enroll_count": obj.course_enrolls.all().count()}


class CourseRetrieveSerializerAfterEnroll(EnrolledSerializerMixin):
    """Serializer for retrieving courses."""

    sessions = CourseSessionSerializer(many=True)
    notes = NoteSerializerAfterEnroll(many=True)
    recorded_videos = RecordedVideoDetailSerializer(many=True)
    physical_books = PhysicalBookSerializerBeforeEnroll(many=True)
    course_enroll = serializers.SerializerMethodField()
    enrollment_count = serializers.SerializerMethodField()

    class Meta:

        model = Course
        fields = (
            "id",
            "name",
            "category",
            "description",
            "course_enroll",
            "image",
            "enrollment_count",
            "status",
            "price",
            "physical_books",
            "duration",
            "sessions",
            "recorded_videos",
            "notes",
        )

    def get_enrollment_count(self, obj):
        return {"course_enroll_count": obj.course_enrolls.all().count()}

    def get_course_enroll(self, obj):
        enrollments = []
        user = self.context["request"].user
        if user.is_authenticated:
            enrollments = obj.enrolls.all().filter(student=user)
        if len(enrollments) > 0:
            enrollment = enrollments.first()
            course_enrollment = enrollment.course_enrolls.filter(course=obj).first()
            if course_enrollment.course_enroll_status != CourseEnrollmentStatus.NEW:
                return CourseEnrollmentCourseRetrieveSerializer(course_enrollment).data
        return None


class CourseRetrieveSerializerBeforeEnroll(EnrolledSerializerMixin):
    """Serializer for retrieving courses."""

    sessions = CourseSessionSerializer(many=True)
    physical_books = PhysicalBookSerializerBeforeEnroll(many=True)
    enrollment_count = serializers.SerializerMethodField()

    class Meta:

        model = Course
        fields = (
            "id",
            "name",
            "status",
            "price",
            "description",
            "category",
            "physical_books",
            "duration",
            "sessions",
            "enrollment_count",
            "image",
        )

    def get_enrollment_count(self, obj):
        return {"course_enroll_count": obj.course_enrolls.all().count()}


class CourseCategoryRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving course categories."""

    # count = serializers.SerializerMethodField()

    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
            # "count",
        )

    # def get_count(self, obj):
    #     cat1 = obj
    #     count = cat1.courses.count()
    #     return count


class CourseCategoryUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating course categories."""

    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
        )


class CourseCategoryDeleteSerializer(serializers.ModelSerializer):
    """Serializer for deleting course categories."""

    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
        )
