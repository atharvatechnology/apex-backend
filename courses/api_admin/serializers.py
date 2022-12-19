from rest_framework import serializers

from common.api.serializers import PublishedSerializer
from courses.models import Course, CourseCategory
from exams.api_admin.serializers import ExamOnCourseRetrieveSerializer


class CourseCategorySerializer(serializers.ModelSerializer):
    """Serializer for creating course categories."""

    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
        )


class CourseSerializer(PublishedSerializer):
    """Serializer for creating courses."""

    exams = ExamOnCourseRetrieveSerializer(
        many=True, source="exams_exam_related", required=False
    )
    created_at = serializers.SerializerMethodField(read_only=True)
    starting_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = PublishedSerializer.Meta.fields + (
            "id",
            "name",
            "status",
            "price",
            "category",
            "description",
            "password",
            "link",
            "image",
            "duration",
            "overview_detail",
            "feature_detail",
            "exams",
            "created_at",
            "starting_date",
        )

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d %b %Y")

    def get_starting_date(self, obj):
        return " ,".join(x.start_date.strftime("%d %b %Y") for x in obj.sessions.all())


class CourseUpdateSerializer(PublishedSerializer):
    """Serializer for updating courses."""

    class Meta:
        model = Course
        fields = PublishedSerializer.Meta.fields + (
            "id",
            "name",
            "status",
            "price",
            "category",
            "description",
            "password",
            "link",
            "image",
            "duration",
            "overview_detail",
            "feature_detail",
            "exams_exam_related",
        )


class ExamInCourseDeleteSerializer(serializers.Serializer):
    """Serializer for deleting exams in courses."""

    exam_id = serializers.IntegerField()
    course_id = serializers.IntegerField()


class CourseOverviewSerializer(PublishedSerializer):
    """Serializer for overview of courses."""

    starting_date = serializers.SerializerMethodField(read_only=True)
    student_enroll = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = PublishedSerializer.Meta.fields + (
            "id",
            "name",
            "status",
            "price",
            "duration",
            "student_enroll",
            "starting_date",
        )

    def get_student_enroll(self, obj):
        return obj.enrolls.all().count()

    def get_starting_date(self, obj):
        return " ,".join(x.start_date.strftime("%d %b %Y") for x in obj.sessions.all())
