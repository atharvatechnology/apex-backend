from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from common.paginations import StandardResultsSetPagination
from courses.api_admin.serializers import (
    CourseCategorySerializer,
    CourseSerializer,
    CourseUpdateSerializer,
    ExamInCourseDeleteSerializer,
)
from courses.api_common.serializers import CourseMinSerializer
from courses.models import Course, CourseCategory


class CourseCategoryCreateAPIView(CreateAPIView):
    """View for creating course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseCategorySerializer


class CourseCategoryListAPIView(ListAPIView):
    """View for listing course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryRetrieveAPIView(RetrieveAPIView):
    """View for retrieving course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryUpdateAPIView(UpdateAPIView):
    """View for updating course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryDeleteAPIView(DestroyAPIView):
    """View for deleting course categories."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CourseCategory.objects.all()


class CourseCreateAPIView(CreateAPIView):
    """View for creating courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseSerializer


class CourseListAPIView(ListAPIView):
    """View for listing courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = StandardResultsSetPagination


class CourseRetrieveAPIView(RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseUpdateAPIView(UpdateAPIView):
    """View for updating courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseUpdateSerializer
    queryset = Course.objects.all()


class CourseDeleteAPIView(DestroyAPIView):
    """View for deleting courses."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Course.objects.all()


class CourseDropdownListAPIView(ListAPIView):
    """View for listing courses for dropdown."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseMinSerializer
    queryset = Course.objects.all()


@swagger_auto_schema(method="POST", request_body=ExamInCourseDeleteSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def remove_exam_in_course(request):
    """View for removing exam relations in course."""
    serializer = ExamInCourseDeleteSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        course_id = serializer.validated_data.get("course_id")
        exam_id = serializer.validated_data.get("exam_id")
        course = Course.objects.get(id=course_id)
        exam = course.exams_exam_related.get(id=exam_id)
        course.exams_exam_related.remove(exam)
        return Response({"message": "Success"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
