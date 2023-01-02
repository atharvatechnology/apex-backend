from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from common.paginations import StandardResultsSetPagination
from common.permissions import IsAccountant, IsAdminorSuperAdminorDirector, IsCashier
from courses.api_admin.serializers import (
    CourseCategorySerializer,
    CourseOverviewSerializer,
    CoursePbookSerilaizer,
    CourseRetrieveCardSerializer,
    CourseSerializer,
    CourseUpdateSerializer,
    ExamInCourseDeleteSerializer,
)
from courses.api_common.serializers import CourseMinSerializer
from courses.filters import CourseDropdownFilter, CourseFilter
from courses.models import Course, CourseCategory


class CourseCategoryCreateAPIView(CreateAPIView):
    """View for creating course categories."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = CourseCategorySerializer


class CourseCategoryListAPIView(ListAPIView):
    """View for listing course categories."""

    permission_classes = [IsAdminorSuperAdminorDirector | IsAccountant | IsCashier]
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryRetrieveAPIView(RetrieveAPIView):
    """View for retrieving course categories."""

    permission_classes = [IsAdminorSuperAdminorDirector | IsAccountant | IsCashier]
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryUpdateAPIView(UpdateAPIView):
    """View for updating course categories."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()


class CourseCategoryDeleteAPIView(DestroyAPIView):
    """View for deleting course categories."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    queryset = CourseCategory.objects.all()


class CourseCreateAPIView(BaseCreatorCreateAPIView):
    """View for creating courses."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = CourseSerializer


class CourseListAPIView(ListAPIView):
    """View for listing courses."""

    permission_classes = [IsAdminorSuperAdminorDirector | IsAccountant | IsCashier]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = CourseFilter
    serializer_class = CourseSerializer
    search_fields = ["name"]
    queryset = Course.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = CourseFilter


class CourseRetrieveAPIView(RetrieveAPIView):
    """View for retrieving courses."""

    permission_classes = [IsAdminorSuperAdminorDirector | IsAccountant | IsCashier]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseRetrieveCardAPIView(RetrieveAPIView):
    permission_classes = [IsAdminorSuperAdminorDirector]
    queryset = Course.objects.all()
    serializer_class = CourseRetrieveCardSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = [
            {
                "title": "Video",
                "data": instance.recorded_videos.all().count(),
            },
            {
                "title": "Exams",
                "data": instance.exams_exam_related.all().count(),
            },
            {"title": "Resources", "data": instance.notes.all().count()},
        ]
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)


class CourseUpdateAPIView(BaseCreatorUpdateAPIView):
    """View for updating courses."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    serializer_class = CourseUpdateSerializer
    queryset = Course.objects.all()


class CourseDeleteAPIView(DestroyAPIView):
    """View for deleting courses."""

    permission_classes = [IsAdminorSuperAdminorDirector]
    queryset = Course.objects.all()


class CourseDropdownListAPIView(ListAPIView):
    """View for listing courses for dropdown."""

    permission_classes = [IsAdminorSuperAdminorDirector | IsAccountant | IsCashier]
    serializer_class = CourseMinSerializer
    filterset_class = CourseDropdownFilter
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    queryset = Course.objects.all()


@swagger_auto_schema(method="POST", request_body=ExamInCourseDeleteSerializer)
@api_view(["POST"])
@permission_classes([IsAdminorSuperAdminorDirector])
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


class CourseOverviewAPIView(CourseListAPIView):
    serializer_class = CourseOverviewSerializer


class CourseOverviewCardAPIView(APIView):
    permission_classes = [IsAdminorSuperAdminorDirector]
    queryset = Course.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        category = CourseCategory.objects.all()
        data = [{"title": "Overall", "data": queryset.all().count()}]
        data.extend(
            {"title": cat.name, "data": queryset.filter(category=cat).count()}
            for cat in category
        )
        return Response(data)


class CourseStudentPBook(ListAPIView):
    permission_classes = [IsAdminorSuperAdminorDirector]
    queryset = Course.objects.all()
    serializer_class = CoursePbookSerilaizer

    def get_queryset(self):
        queryset = super().get_queryset()
        from enrollments.models import EnrollmentStatus

        student_id = self.kwargs.get("student_id")
        return queryset.filter(
            enrolls__student__id=student_id, enrolls__status=EnrollmentStatus.ACTIVE
        )
