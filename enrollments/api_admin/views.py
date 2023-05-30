from django.contrib.auth import get_user_model
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from common.api.views import (
    BaseCreatorCreateAPIView,
    BaseCreatorUpdateAPIView,
    BaseReportGeneratorAPIView,
)
from common.paginations import StandardResultsSetPagination
from common.permissions import (
    IsAccountant,
    IsAdminOrSuperAdminOrDirector,
    IsCashier,
    IsContentCreator,
)
from common.utils import decode_user
from courses.api.serializers import CourseCategoryRetrieveSerializer
from courses.filters import CourseFilter
from courses.models import CourseCategory
from enrollments.api.serializers import CourseEnrollmentSerializer
from enrollments.api_admin.serializers import (
    CourseEnrollmentCreateSerializer,
    CourseSessionAdminSerializer,
    CourseSessionAdminUpdateSerializer,
    CourseThroughEnrollmentAdminBaseSerializer,
    CourseThroughEnrollmentAdminStudentSerializer,
    EnrollmentStatusAdminUpdateSerializer,
    ExamEnrollmentCreateSerializer,
    ExamSessionAdminSerializer,
    ExamSessionAdminUpdateSerializer,
    ExamThroughEnrollmentAdminListSerializer,
    GetAllEnrollmentSerializer,
    GetCourseEnrollmentByUserSerializer,
    PhysicalBookCourseEnrollmentAdminSerializer,
    PhysicalBookCourseEnrollmentCreateAdminSerializer,
    PhysicalBookCourseEnrollmentUpdateAdminSerializer,
    StudentEnrollmentCheckSerializer,
)
from enrollments.filters import (
    CourseGraphFilter,
    CourseThroughEnrollmentFilter,
    ExamThroughEnrollmentFilter,
)
from enrollments.models import (
    CourseSession,
    CourseThroughEnrollment,
    Enrollment,
    EnrollmentStatus,
    ExamSession,
    ExamThroughEnrollment,
    PhysicalBookCourseEnrollment,
    SessionStatus,
)
from exams.models import Exam

User = get_user_model()


class GetCourseEnrollmentByUserAPIView(GenericAPIView):
    serializer_class = GetCourseEnrollmentByUserSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector]

    def get(self, request, *args, **kwargs):
        decoded_user = None
        if student_code := self.kwargs.get("student_code"):
            decoded_user = decode_user(student_code)
        user_object = None
        if decoded_user is not None:
            user_object = User.objects.filter(username=decoded_user).first()

        enrollments = CourseThroughEnrollment.objects.filter(
            enrollment__student=user_object,
            selected_session__status=SessionStatus.ACTIVE,
        )
        data = {"user": user_object, "enrollments": enrollments}
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class ExamSessionCreateAPIView(BaseCreatorCreateAPIView):
    """Create a new session for an exam."""

    serializer_class = ExamSessionAdminSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector]


class ExamSessionUpdateAPIView(BaseCreatorUpdateAPIView):
    """Update an existing session for an exam."""

    serializer_class = ExamSessionAdminUpdateSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = ExamSession.objects.all()

    def can_update_object(self, obj):
        """Check if the user can update the object.

        Raises a PermissionDenied exception
            if the user cannot update a session which is ended.
        """
        if obj.end_date < timezone.now():
            self.permission_denied(
                self.request, message="Cannot update a session which is ended."
            )

    def get_object(self):
        obj = super().get_object()
        self.can_update_object(obj)
        return obj


class ExamSessionListAPIView(ListAPIView):
    """List all sessions for an exam."""

    serializer_class = ExamSessionAdminSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsAccountant | IsCashier]
    queryset = ExamSession.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(exam__id=self.kwargs["exam_id"])


class ExamSessionDeleteAPIView(DestroyAPIView):
    """Delete an existing session for an exam."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = ExamSession.objects.all()

    def can_delete(self, object):
        """Check if the user can delete the object.

        Raises a PermissionDenied exception
            if the user cannot delete a session which is ended.
        """
        if object.start_date < timezone.now():
            self.permission_denied(
                self.request,
                message="Cannot delete a session that has already started.",
            )

    def get_object(self):
        obj = super().get_object()
        self.can_delete(obj)
        return obj


class ExamGraphAPIView(ListAPIView):
    """Exam enrollment(Frame 222) graph with number of students enrolled to exam."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamThroughEnrollmentAdminListSerializer

    def get(self, *args, **kwargs):
        exams = Exam.objects.all()
        final = {}
        for exam in exams:
            enrollment_count, exam_name = (
                super().get_queryset().filter(exam__id=exam.id).count(),
                exam.name,
            )
            if enrollment_count > 0:
                final[exam_name] = enrollment_count
        return Response({"exam_graph": final}, status=status.HTTP_200_OK)


# Course Session starts


class CourseSessionCreateAPIView(BaseCreatorCreateAPIView):
    """Create a new session for an exam."""

    serializer_class = CourseSessionAdminSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class CourseSessionUpdateAPIView(BaseCreatorUpdateAPIView):
    """Update an existing session for an exam."""

    serializer_class = CourseSessionAdminUpdateSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]
    queryset = CourseSession.objects.all()

    def can_update_object(self, obj):
        """Check if the user can update the object.

        Raises a PermissionDenied exception
            if the user cannot update a session which is ended.
        """
        if obj.end_date < timezone.now():
            self.permission_denied(
                self.request, message="Cannot update a session which is ended."
            )

    def get_object(self):
        obj = super().get_object()
        self.can_update_object(obj)
        return obj


class CourseSessionListAPIView(ListAPIView):
    """List all sessions for an exam."""

    serializer_class = CourseSessionAdminSerializer
    permission_classes = [
        IsAdminOrSuperAdminOrDirector | IsAccountant | IsCashier | IsContentCreator
    ]
    queryset = CourseSession.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(course__id=self.kwargs["course_id"])


class CourseSessionDeleteAPIView(DestroyAPIView):
    """Delete an existing session for an exam."""

    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]
    queryset = CourseSession.objects.all()

    def can_delete(self, object):
        """Check if the user can delete the object.

        Raises a PermissionDenied exception
            if the user cannot delete a session which is ended.
        """
        if object.start_date < timezone.now():
            self.permission_denied(
                self.request,
                message="Cannot delete a session that has already started.",
            )

    def get_object(self):
        obj = super().get_object()
        self.can_delete(obj)
        return obj


class CourseGraphAPIView(ListAPIView):
    """Bar Graph based on category including course."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategoryRetrieveSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CourseGraphFilter

    def get(self, *args, **kwargs):
        new_list = []
        course_category = self.filter_queryset(self.get_queryset())
        for category in course_category:
            course_list = []
            for course in category.courses.all():
                enrollment_count = course.enrolls.all().count()
                if enrollment_count != 0:
                    course_list.append({course.name: enrollment_count})
            if len(course_list):
                new_list.append({category.name: course_list})
        return Response(new_list, status=status.HTTP_200_OK)


# course session ends
class EnrollmentGraphAPIView(ListAPIView):
    """Graph based on enrollment to the course."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer

    def get(self, *args, **kwargs):
        new_list = []
        total_enrollment = 0
        course_category = CourseCategory.objects.all()
        for category in course_category:
            for course in category.courses.all():
                enrollment_count = course.enrolls.filter(
                    status=EnrollmentStatus.ACTIVE
                ).count()
                total_enrollment += enrollment_count
            if total_enrollment != 0:
                new_list.append({category.name: total_enrollment})
            total_enrollment = 0
        return Response(new_list, status=status.HTTP_200_OK)


class OverallEnrollmentAPIView(ListAPIView):
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer

    def get(self, *args, **kwargs):
        total_active_enrollment = 0
        total_enrollment = 0
        course_category = CourseCategory.objects.all()
        for category in course_category:
            for course in category.courses.all():
                active_enrollment = course.enrolls.filter(
                    status=EnrollmentStatus.ACTIVE
                ).count()
                enrollment = course.enrolls.all().count()
                total_enrollment += enrollment
                total_active_enrollment += active_enrollment
        new_list = [
            {
                "active_enrollment": total_active_enrollment,
                "total_enrollment": total_enrollment,
            }
        ]
        return Response(new_list, status=status.HTTP_200_OK)


class ExamEnrollmentCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    serializer_class = ExamEnrollmentCreateSerializer
    queryset = Enrollment.objects.all()


class CourseEnrollmentCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    serializer_class = CourseEnrollmentCreateSerializer
    queryset = Enrollment.objects.all()


class ExamThroughEnrollmentListAPIView(ListAPIView):
    """List all student in Exam."""

    serializer_class = ExamThroughEnrollmentAdminListSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    queryset = ExamThroughEnrollment.objects
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    pagination_class = StandardResultsSetPagination
    search_fields = [
        "enrollment__student__first_name",
        "enrollment__student__last_name",
        "enrollment__student__username",
        "exam__name",
    ]
    ordering_fields = ["status", "score"]
    filterset_class = ExamThroughEnrollmentFilter


class ExamThroughEnrollmentListCardAPIView(APIView):
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    queryset = Enrollment.objects.filter(exams__isnull=False)

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        data = [
            {"title": "Enrollments", "data": queryset.count()},
            {
                "title": "Verified Enrollments",
                "data": queryset.filter(status=EnrollmentStatus.ACTIVE).count(),
            },
            {
                "title": "Pending Enrollments",
                "data": queryset.filter(status=EnrollmentStatus.PENDING).count(),
            },
        ]
        return Response(data)


class CourseThroughEnrollmentListAPIView(ListAPIView):
    """List all student in Course."""

    serializer_class = CourseThroughEnrollmentAdminBaseSerializer
    permission_classes = [
        IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant | IsContentCreator
    ]
    filterset_class = CourseFilter
    queryset = CourseThroughEnrollment.objects.order_by("-enrollment__created_at")
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    pagination_class = StandardResultsSetPagination
    search_fields = [
        "enrollment__student__first_name",
        "enrollment__student__last_name",
        "enrollment__student__username",
        "course__name",
    ]
    # ordering_fields = ["status", "score"]
    filterset_class = CourseThroughEnrollmentFilter


class CourseThroughEnrollmentStudentListAPIView(ListAPIView):
    """List all student in Course."""

    serializer_class = CourseThroughEnrollmentAdminStudentSerializer
    permission_classes = [
        IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant | IsContentCreator
    ]
    filterset_class = CourseFilter
    queryset = CourseThroughEnrollment.objects.order_by("-enrollment__created_at")
    filter_backends = [
        DjangoFilterBackend,
    ]
    pagination_class = StandardResultsSetPagination
    filterset_class = CourseThroughEnrollmentFilter

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        return super().get_queryset().filter(enrollment__student_id=student_id)


class CourseThroughEnrollmentCourseWiseListAPIView(CourseThroughEnrollmentListAPIView):
    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return super().get_queryset().filter(course__id=course_id)


class CourseThroughEnrollmentListCardAPIView(APIView):
    permission_classes = [
        IsAccountant | IsAdminOrSuperAdminOrDirector | IsCashier | IsContentCreator
    ]
    queryset = Enrollment.objects.filter(courses__isnull=False)

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        data = [
            {"title": "Enrollments", "data": queryset.count()},
            {
                "title": "Verified Enrollments",
                "data": queryset.filter(status=EnrollmentStatus.ACTIVE).count(),
            },
            {
                "title": "Pending Enrollments",
                "data": queryset.filter(status=EnrollmentStatus.PENDING).count(),
            },
        ]
        return Response(data)


class EnrollmentUpdateAdminAPIView(UpdateAPIView):
    """Update an existing enrollment."""

    serializer_class = EnrollmentStatusAdminUpdateSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsAccountant]
    queryset = Enrollment.objects.all()


class EnrollmentDeleteAdminAPIView(DestroyAPIView):
    """Delete student enrollment."""

    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    queryset = Enrollment.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_cashier and instance.status == EnrollmentStatus.PENDING:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentCourseCheckView(GenericAPIView):
    """View for checking if student is enrolled in a course."""

    permission_classes = [
        IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant | IsContentCreator
    ]
    serializer_class = StudentEnrollmentCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"status": "success", "message": "Student is enrolled in the course."}
        )


class PhysicalBookCourseEnrollmentAdminCreateAPIView(CreateAPIView):
    """Create physical book after course enrollment."""

    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentCreateAdminSerializer


class PhysicalBookCourseEnrollmentAdminListAPIView(ListAPIView):
    """Physical book list after user course enrolled."""

    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    search_fields = ["name"]
    filter_backends = [SearchFilter]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentAdminSerializer


class PhysicalBookCourseEnrollmentAdminRetrieveAPIView(RetrieveAPIView):
    """Retrieve physical book after course enrollment."""

    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentAdminSerializer


class PhysicalBookCourseEnrollmentAdminUpdateAPIView(UpdateAPIView):
    """Update physical book after course enrollment."""

    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentUpdateAdminSerializer


class PhysicalBookCourseEnrollmentAdminDestroyAPIView(DestroyAPIView):
    """Destroy physical book after course enrollment."""

    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentAdminSerializer


class ExamThroughEnrollmentGeneratorAPIView(BaseReportGeneratorAPIView):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [
        "enrollment__student__first_name",
        "enrollment__student__last_name",
        "enrollment__student__username",
        "exam__name",
    ]
    queryset = ExamThroughEnrollment.objects.all()
    filterset_class = ExamThroughEnrollmentFilter
    model_name = "ExamThroughEnrollment"

    def get(self, request):
        return Response(
            {
                "model_fields": [
                    "enrollment",
                    "phone_number",
                    "exam",
                    "created_date",
                    "payment",
                    # "rank",
                    # "score",
                    # "negative_score",
                    "status",
                ]
            }
        )


class CourseThroughEnrollmentGeneratorAPIView(BaseReportGeneratorAPIView):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [
        "enrollment__student__first_name",
        "enrollment__student__last_name",
        "enrollment__student__username",
        "course__name",
    ]
    queryset = CourseThroughEnrollment.objects.all().order_by("-enrollment__created_at")
    filterset_class = CourseThroughEnrollmentFilter
    model_name = "CourseThroughEnrollment"

    def get(self, request):
        return Response(
            {
                "model_fields": [
                    "enrollment",
                    "phone_number",
                    "course_name",
                    "created_date",
                    "payment",
                    "course_enroll_status",
                ]
            }
        )


class ExamResultReportGeneratorAPIView(BaseReportGeneratorAPIView):
    queryset = ExamThroughEnrollment.objects
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        "enrollment__student__first_name",
        "enrollment__student__last_name",
        "enrollment__student__username",
        "exam__name",
    ]
    filterset_class = ExamThroughEnrollmentFilter
    model_name = "ExamResult"

    def get(self, request):
        return Response(
            {
                "model_fields": [
                    "student_name",
                    "rank",
                    "score",
                    "negative_score",
                    "status",
                ]
            }
        )


class GetEnrollmentsByUserAPIView(GenericAPIView):
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsAccountant]
    queryset = Enrollment.objects.all()
    serializer_class = GetAllEnrollmentSerializer

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")

        enrollments = Enrollment.objects.filter(student_id=student_id)
        data = {
            "course": CourseThroughEnrollment.objects.filter(
                enrollment__in=enrollments
            ),
            "exam": ExamThroughEnrollment.objects.filter(enrollment__in=enrollments),
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)
