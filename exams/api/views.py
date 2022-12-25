from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime, now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from common.api.mixin import PublishableModelMixin
from common.paginations import StandardResultsSetPagination
from enrollments.models import ExamSession, ExamThroughEnrollment, SessionStatus
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


class ExamListAPIView(PublishableModelMixin, ListAPIView):
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        exam_session = ExamSession.objects.filter(
            exam=instance, id=self.kwargs["session_id"]
        ).first()
        enrollment = ExamThroughEnrollment.objects.filter(
            selected_session=exam_session, enrollment__student=self.request.user
        ).first()
        if enrollment:
            if enrollment.selected_session.status == SessionStatus.ACTIVE:
                return super().retrieve(request, *args, **kwargs)
            return Response({"detail": "Exam Session is not Active"}, status=400)
        return Response(
            "Student is not enrolled to {} exam session.".format(
                self.kwargs["session_id"]
            )
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
    exm_enr = ExamThroughEnrollment.objects.filter(
        enrollment__student=user, exam=exam
    ).latest("id")
    exm_sess = exm_enr.selected_session
    # Check if the latest exam session is active
    if exm_sess.status != SessionStatus.ACTIVE:
        return Response({"detail": "Exam session is not active."})
    # Trigger session end which must trigger exam submit
    if exm_sess.end_date > localtime(now()):
        return Response({"detail": "Exam session is not over yet."})
    exm_sess.end_session()
    return Response({"detail": "Exam submitted successfully."})
