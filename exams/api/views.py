from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime, now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from common.api.mixin import InterestWiseOrderMixin, PublishableModelMixin
from common.paginations import StandardResultsSetPagination
from enrollments.models import Enrollment, ExamThroughEnrollment, SessionStatus
from exams.api.permissions import IsExamEnrolledActive
from exams.filters import ExamFilter
from exams.models import Exam

from .serializers import (  # ExamUpdateSerializer,
    ExamListSerializer,
    ExamPaperSerializer,
    ExamRetrievePoolSerializer,
    ExamRetrieveSerializer,
)

# from common.utils import excelgenerator

# class ExamCreateAPIView(BaseCreatorCreateAPIView):
#     serializer_class = ExamCreateSerializer
#     # permission_classes = [AllowAny]


class ExamListAPIView(PublishableModelMixin, InterestWiseOrderMixin, ListAPIView):
    """View for listing exams."""

    serializer_class = ExamListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()
    filterset_class = ExamFilter
    search_fields = ["name"]
    pagination_class = StandardResultsSetPagination


class ExamRetrieveAPIView(PublishableModelMixin, RetrieveAPIView):
    """View for retrieving exams."""

    serializer_class = ExamRetrieveSerializer
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()


class ExamRetrievePoolAPIView(RetrieveAPIView):
    serializer_class = ExamRetrievePoolSerializer
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()


# class ExamUpdateAPIView(BaseCreatorUpdateAPIView):
#     serializer_class = ExamUpdateSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Exam.objects.all()


class ExamPaperAPIView(RetrieveAPIView):
    serializer_class = ExamPaperSerializer
    permission_classes = [IsAuthenticated, IsExamEnrolledActive]  # TODO: IsEnrolled
    queryset = Exam.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("template").prefetch_related(
            "questions__options"
        )
        # .prefetch_related("questions__options")
        # .prefetch_related("category")
        return queryset

    def _get_student_enrollment(self, obj):
        if not hasattr(self, "_student_enrollment"):
            try:
                student_enrollment = obj.enrolls.filter(
                    student=self.request.user
                ).latest("id")
            except Enrollment.DoesNotExist:
                student_enrollment = None
            self._student_enrollment = student_enrollment
        return self._student_enrollment

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student_enrollment = self._get_student_enrollment(instance)
        if student_enrollment:
            try:
                student_through_enrollment = (
                    student_enrollment.exam_enrolls.select_related(
                        "selected_session"
                    ).latest("id")
                )
            except ExamThroughEnrollment.DoesNotExist:
                student_through_enrollment = None
            request.student_through_enrollment = student_through_enrollment
            session = student_through_enrollment.selected_session
            session_status = session.status
            if session_status == SessionStatus.ACTIVE:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            return Response({"detail": "Exam Session is not Active"}, status=400)
        return Response(
            f'Student is not enrolled to {self.kwargs["session_id"]} exam session.'
        )


class ExamPaperPreviewAPIView(RetrieveAPIView):
    serializer_class = ExamPaperSerializer
    permission_classes = [IsAdminUser]
    queryset = Exam.objects.all()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def trigger_exam_submit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    # Check if exam is of practice type
    if not exam.is_practice:
        return Response({"detail": "Cannot trigger exam not of practice type."})
    # retrieve user
    user = request.user
    # Find the latest exam enrollment of the user
    try:
        exm_enr = ExamThroughEnrollment.objects.filter(
            enrollment__student=user, exam=exam
        ).latest("id")
    except ExamThroughEnrollment.DoesNotExist:
        return Response({"detail": "Exam enrollment not found."}, status=404)
    exm_sess = exm_enr.selected_session
    # Check if the latest exam session is active
    if exm_sess.status != SessionStatus.ACTIVE:
        return Response({"detail": "Exam session is not active."})
    # Trigger session end which must trigger exam submit
    if exm_sess.end_date > localtime(now()):
        return Response({"detail": "Exam session is not over yet."})
    exm_sess.end_session()
    return Response({"detail": "Exam submitted successfully."})
