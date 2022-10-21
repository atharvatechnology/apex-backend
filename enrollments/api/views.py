import base64
import io

import xlsxwriter
from django.http import HttpResponse
from django.utils.timezone import localtime
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from common.utils import dynamic_excel_generator
from enrollments.api.serializers import (
    CourseEnrollmentRetrieveSerializer,
    CourseEnrollmentSerializer,
    CourseEnrollmentUpdateSerializer,
    EnrollmentCreateSerializer,
    EnrollmentRetrieveSerializer,
    ExamEnrollmentCheckPointRetrieveSerializer,
    ExamEnrollmentRetrievePoolSerializer,
    ExamEnrollmentRetrieveSerializer,
    ExamEnrollmentUpdateSerializer,
    PhysicalBookCourseEnrollmentSerializer,
    StudentEnrollmentSerializer,
)

# from enrollments.api.tasks import Excelcelery
# from enrollments.filters import ExamThroughEnrollmentFilter
from enrollments.models import (
    CourseThroughEnrollment,
    Enrollment,
    ExamEnrollmentStatus,
    ExamThroughEnrollment,
    PhysicalBookCourseEnrollment,
    SessionStatus,
)
from enrollments.report import ExamThroughEnrollmentTableData


class EnrollmentCreateAPIView(CreateAPIView):
    """Create a new enrollment for a student."""

    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentCreateSerializer
    queryset = Enrollment.objects.all()

    def perform_create(self, serializer):
        """Create a new enrollment for the current user.

        Parameters
        ----------
        serializer : EnrollmentCreateSerializer
            Serializer for the enrollment creation.

        Returns
        -------
        Enrollment
            The newly created enrollment.

        """
        return serializer.save(student=self.request.user)


class EnrollmentListAPIView(ListAPIView):
    """List all enrollments for a student."""

    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentRetrieveSerializer
    queryset = Enrollment.objects.all()

    def get_queryset(self):
        """Get the enrollments for the current user.

        Returns
        -------
        QuerySet
            The set of enrollments of the current user.

        """
        queryset = super().get_queryset()
        return queryset.filter(student=self.request.user)


class ExamEnrollmentUpdateAPIView(UpdateAPIView):
    """Submit an exam enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentUpdateSerializer

    def update(self, request, *args, **kwargs):
        exam_enrollment = self.get_object()
        if exam_enrollment.status != ExamEnrollmentStatus.CREATED:
            return Response(
                {"detail": "Your answers have already been submitted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)


class ExamEnrollmentRetrieveAPIView(RetrieveAPIView):
    """Retrieve an exam enrollment result."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        exam_enrollment = self.get_object()
        # if (
        #     # the exam is still in progress
        #     exam_enrollment.selected_session.status
        #     == SessionStatus.ENDED
        # ) and (
        #     # the exam result has not been calculated yet
        #     exam_enrollment.status
        #     in [ExamEnrollmentStatus.FAILED, ExamEnrollmentStatus.PASSED]
        # ):
        selected_session = exam_enrollment.selected_session
        if selected_session.is_visible and (
            selected_session.status == SessionStatus.RESULTSOUT
        ):
            # if (selected_session.status == SessionStatus.RESULTSOUT):
            return super().retrieve(request, *args, **kwargs)
        if publish_date := selected_session.result_publish_date:
            error_detail = f"Your result will be published \
                on {localtime(publish_date).strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            error_detail = "Your result has not been published yet."

        return Response(
            {"detail": error_detail},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ExamEnrollmentCheckpointRetrieveAPIView(RetrieveAPIView):
    """Retrieve an exam enrollment saved state."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentCheckPointRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        exam_enrollment = self.get_object()
        if (
            # the exam is still in progress
            exam_enrollment.selected_session.status
            == SessionStatus.ACTIVE
        ) and (
            # the exam result has not been calculated yet
            exam_enrollment.status
            in [ExamEnrollmentStatus.CREATED]
        ):
            return super().retrieve(request, *args, **kwargs)

        return Response(
            {"detail": "Exam is not active or u have already submitted."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ExamEnrollmentRetrievePoolAPIView(RetrieveAPIView):
    """Retrieve an exam enrollment result."""

    permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentRetrievePoolSerializer


class PhysicalBookCourseEnrollmentListAPIView(ListAPIView):
    """Physical book list after user course enrolled."""

    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class PhysicalBookCourseEnrollmentCreateAPIView(CreateAPIView):
    """Create physical book after course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class PhysicalBookCourseEnrollmentRetrieveAPIView(RetrieveAPIView):
    """Retrieve physical book after course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class PhysicalBookCourseEnrollmentUpdateAPIView(UpdateAPIView):
    """Update physical book after course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class PhysicalBookCourseEnrollmentDestroyAPIView(DestroyAPIView):
    """Destroy physical book after course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = PhysicalBookCourseEnrollment.objects.all()
    serializer_class = PhysicalBookCourseEnrollmentSerializer


class CourseEnrollementListAPIView(ListAPIView):
    """List view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer


class CourseEnrollementUpdateAPIView(UpdateAPIView):
    """Update view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentUpdateSerializer


class CourseEnrollementRetrieveAPIView(RetrieveAPIView):
    """Retrieve view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentRetrieveSerializer


class CourseEnrollementDestroyAPIView(DestroyAPIView):
    """Destroy view for course enrollment."""

    permission_classes = [IsAuthenticated]
    queryset = CourseThroughEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer


class CheckIfStudentInCourse(CreateAPIView):
    serializer_class = StudentEnrollmentSerializer


# class ExamThroughEnrollmentGeneratorAPIView(ListAPIView):
#     # permission_classes = [IsAuthenticated]
#     # queryset = ExamThroughEnrollment.objects.all()
#     # serializer_class = ExamEnrollmentRetrievePoolSerializer
#     # model = ExamThroughEnrollment
#     # filter_backends = [DjangoFilterBackend]
#     # filterset_class = ExamThroughEnrollmentFilter

#     def list(self, request, *args, **kwargs):
#         model_fields = request.GET.get('model_fields')
#         model_name = request.GET.get('model_name')
# model_fields = [
#     "enrollment",
#     "exam",
#     "selected_session",
#     "score",
#     "negative_score",
#     "status"
# ]
#         qs= list(self.get_queryset().values_list("id", flat=True))
#         Excelcelery(model_name,model_fields)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)


def dynamic_excel_generator():
    # Create a workbook and add a worksheet.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {"in_memory": True})
    worksheet = workbook.add_worksheet("report")
    # bold = workbook.add_format({"bold": True})
    # Some data we want to write to the worksheet.
    # passing field names received from front-end

    model_fields = [
        "enrollment",
        "exam",
        "selected_session",
        "exam_questions",
        "score",
        "negative_score",
        "status",
    ]
    # get model names and it correcponding headers needed in report.
    exam_through_enrollment = ExamThroughEnrollmentTableData(
        model_fields, ExamThroughEnrollment.objects.all(), worksheet
    )
    worksheet = exam_through_enrollment.generate_report()
    workbook.close()

    output.seek(0)

    blob = base64.b64encode(output.read())
    response = HttpResponse(blob, content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment; filename=report.xlsx"

    return response


class ExamThroughEnrollmentGeneratorAPIView(APIView):
    def get(self, request):
        # dynamic_excel_generator(self.model.__name__,queryset)
        # queryset = ExamThroughEnrollment.objects.all()
        # file_handle = queryset.file.path
        # document = open(file_handle, 'rb')
        # response = HttpResponse(FileWrapper(document), content_type='')
        # response['Content-Disposition']=f'attachment; filename="{queryset.file.name}"'
        return HttpResponse()
