from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from courses.api.paginations import StandardResultsSetPagination
from exams.api.permissions import IsExamEnrolledActive
from exams.models import Exam, ExamStatus, ExamTemplate, Section

from .serializers import (
    ExamCreateSerializer,
    ExamListSerializer,
    ExamPaperSerializer,
    ExamRetrievePoolSerializer,
    ExamRetrieveSerializer,
    ExamTemplateRetrieveSerializer,
    ExamTemplateSerializer,
    ExamUpdateSerializer,
    SectionSerializer,
)


class ExamCreateAPIView(BaseCreatorCreateAPIView):
    serializer_class = ExamCreateSerializer
    # permission_classes = [AllowAny]


class ExamListAPIView(ListAPIView):
    serializer_class = ExamListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()
    pagination_class = StandardResultsSetPagination


class ExamRetrieveAPIView(RetrieveAPIView):
    serializer_class = ExamRetrieveSerializer
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()


class ExamRetrievePoolAPIView(RetrieveAPIView):
    serializer_class = ExamRetrievePoolSerializer
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()


class ExamUpdateAPIView(BaseCreatorUpdateAPIView):
    serializer_class = ExamUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()


class ExamPaperAPIView(RetrieveAPIView):
    serializer_class = ExamPaperSerializer
    permission_classes = [IsAuthenticated, IsExamEnrolledActive]  # TODO: IsEnrolled
    queryset = Exam.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == ExamStatus.IN_PROGRESS:
            return super().retrieve(request, *args, **kwargs)
        return Response({"detail": "Exam is not in progress"}, status=400)


class ExamPaperPreviewAPIView(RetrieveAPIView):
    serializer_class = ExamPaperSerializer
    permission_classes = [IsAdminUser]
    queryset = Exam.objects.all()


class ExamDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()


class ExamTemplateCreateAPIView(BaseCreatorCreateAPIView):
    serializer_class = ExamTemplateSerializer
    permission_classes = []


class ExamTemplateListAPIView(ListAPIView):
    serializer_class = ExamTemplateSerializer
    # TODO: permit admin only
    # permission_classes = []
    queryset = ExamTemplate.objects.all()


class ExamTemplateRetrieveAPIView(RetrieveAPIView):
    serializer_class = ExamTemplateRetrieveSerializer
    queryset = ExamTemplate.objects.all()


class ExamTemplateUpdateAPIView(BaseCreatorUpdateAPIView):
    serializer_class = ExamTemplateSerializer
    # TODO: permit admin only
    permission_classes = []
    queryset = ExamTemplate.objects.all()


class ExamTemplateDeleteAPIView(DestroyAPIView):
    # TODO: permit admin only
    permission_classes = []
    # permission_classes = [IsAuthenticated]
    queryset = ExamTemplate.objects.all()


class SectionCreateAPIView(CreateAPIView):
    serializer_class = SectionSerializer
    # permission_classes =


class SectionUpdateAPIView(UpdateAPIView):
    serializer_class = SectionSerializer
    # permission_classes =
    queryset = Section.objects.all()


class SectionDeleteAPIView(DestroyAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    # permission_classes =
