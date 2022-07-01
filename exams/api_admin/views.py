from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from courses.api.paginations import StandardResultsSetPagination
from exams.models import Exam, ExamTemplate, ExamTemplateStatus, Question, Section

from .serializers import (
    ExamCreateSerializer,
    ExamListAdminSerializer,
    ExamRetrieveAdminSerializer,
    ExamTemplateCreateUpdateSerializer,
    ExamTemplateMiniSerializer,
    ExamTemplateRetrieveSerializer,
    ExamUpdateSerializer,
    OptionCUDSerializer,
    QuestionCreateSerializer,
    QuestionUpdateSerializer,
    SectionCRUDSerializer,
)


class QuestionCreateAPIView(CreateAPIView):
    serializer_class = QuestionCreateSerializer


class QuestionUpdateAPIView(UpdateAPIView):
    serializer_class = QuestionUpdateSerializer
    queryset = Question.objects.all()


class SectionCreateAPIView(CreateAPIView):
    serializer_class = SectionCRUDSerializer
    # permission_classes =


class SectionUpdateAPIView(UpdateAPIView):
    serializer_class = SectionCRUDSerializer
    # permission_classes =
    queryset = Section.objects.all()


class SectionDeleteAPIView(DestroyAPIView):
    serializer_class = SectionCRUDSerializer
    queryset = Section.objects.all()
    # permission_classes =


class ExamTemplateCreateAPIView(BaseCreatorCreateAPIView):
    serializer_class = ExamTemplateCreateUpdateSerializer
    permission_classes = []


class ExamTemplateDropdownListAPIView(ListAPIView):
    serializer_class = ExamTemplateMiniSerializer
    queryset = ExamTemplate.objects.all()
    permission_classes = []

    def get_queryset(self):
        return super().get_queryset().filter(status=ExamTemplateStatus.COMPLETED)


class ExamTemplateListAPIView(ListAPIView):
    serializer_class = ExamTemplateCreateUpdateSerializer
    # TODO: permit admin only
    # permission_classes = []
    queryset = ExamTemplate.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    pagination_class = StandardResultsSetPagination


class ExamTemplateRetrieveAPIView(RetrieveAPIView):
    serializer_class = ExamTemplateRetrieveSerializer
    queryset = ExamTemplate.objects.all()


class ExamTemplateUpdateAPIView(BaseCreatorUpdateAPIView):
    serializer_class = ExamTemplateCreateUpdateSerializer
    # TODO: permit admin only
    permission_classes = []
    queryset = ExamTemplate.objects.all()


class ExamTemplateDeleteAPIView(DestroyAPIView):
    # TODO: permit admin only
    permission_classes = []
    # permission_classes = [IsAuthenticated]
    queryset = ExamTemplate.objects.all()


class OptionCreateAPIView(CreateAPIView):
    serializer_class = OptionCUDSerializer
    # permission_classes =


class OptionUpdateAPIView(UpdateAPIView):
    serializer_class = OptionCUDSerializer
    # permission_classes =
    queryset = Question.objects.all()


class OptionsDeleteAPIView(DestroyAPIView):
    serializer_class = OptionCUDSerializer
    # permission_classes =
    queryset = Question.objects.all()


class QuestionDeleteAPIView(DestroyAPIView):
    queryset = Question.objects.all()


class ExamCreateAPIView(BaseCreatorCreateAPIView):
    serializer_class = ExamCreateSerializer
    # permission_classes = [AllowAny]


class ExamUpdateAPIView(BaseCreatorUpdateAPIView):
    serializer_class = ExamUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()


class ExamDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()


class ExamListAPIView(ListAPIView):
    serializer_class = ExamListAdminSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()
    pagination_class = StandardResultsSetPagination


class ExamRetrieveAPIView(RetrieveAPIView):
    serializer_class = ExamRetrieveAdminSerializer
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()
