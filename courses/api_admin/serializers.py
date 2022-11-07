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

    exams = ExamOnCourseRetrieveSerializer(many=True, source="exams_exam_related")

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
        )
