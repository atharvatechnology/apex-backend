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
from enrollments.api.tasks import Excelcelery

from enrollments.models import (
    CourseThroughEnrollment,
    Enrollment,
    ExamEnrollmentStatus,
    ExamThroughEnrollment,
    PhysicalBookCourseEnrollment,
    SessionStatus,
)
from common.utils import excelgenerator
from django_filters.rest_framework import DjangoFilterBackend

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

class ExamThroughEnrollmentGeneratorAPIView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = ExamThroughEnrollment.objects.all()
    serializer_class = ExamEnrollmentRetrievePoolSerializer
    model = ExamThroughEnrollment
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "exam",
    ]    
    def list(self, request, *args, **kwargs):
        id = request.GET.get('pk')
        if id:
            data = self.get_queryset().filter(id=id)
            queryset = data
        else:    
            queryset = self.filter_queryset(self.get_queryset())
        qs= list(queryset.values_list("id", flat=True))
        Excelcelery(self.model.__name__,qs)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


import xlsxwriter
import io
from django.http import HttpResponse


def dynamic_excel_generator(request):
    # Create a workbook and add a worksheet.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Reporte3a5')
    bold = workbook.add_format({'bold': True})
    # Some data we want to write to the worksheet.
    reporte = ExamThroughEnrollment.objects.all() #my model
    pass
    # Start from the first cell. Rows and columns are zero indexed.
    worksheet.write(0, 0,'S.No')
    worksheet.write(0, 1,'Student Name')
    worksheet.write(0, 2,'Exam')
    worksheet.write(0, 3,'Selected Session')
    row = 1
    col = 0

    # Iterate over the data and write it out row by row.
    for linea in reporte:
        worksheet.write(row, col, row)
        worksheet.write(row, col + 1, str(linea.enrollment.student.first_name)+str(linea.enrollment.student.last_name))
        worksheet.write(row, col + 2, linea.exam.name)
        worksheet.write(row, col + 3, str(linea.selected_session.start_date))
        row += 1

    # Write the title for every column in bold
    # worksheet.write('A1', 'Priority', bold)
    # worksheet.write('B1', 'Code', bold)

    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=Reporte3a5.xlsx"

    return response