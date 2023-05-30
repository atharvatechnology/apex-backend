from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response

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
from exams.filters import ExamOnCourseFilter
from exams.models import Exam, ExamTemplate, ExamTemplateStatus, Question, Section

from ..api_common.serializers import ExamMiniSerializer
from .serializers import (
    ExamCreateSerializer,
    ExamDetailSerializer,
    ExamImageAdminSerializer,
    ExamListAdminSerializer,
    ExamListOverviewAdminSerializer,
    ExamOverviewCardSerializer,
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
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class QuestionUpdateAPIView(UpdateAPIView):
    serializer_class = QuestionUpdateSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class SectionCreateAPIView(CreateAPIView):
    serializer_class = SectionCRUDSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class SectionUpdateAPIView(UpdateAPIView):
    serializer_class = SectionCRUDSerializer
    queryset = Section.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class SectionDeleteAPIView(DestroyAPIView):
    serializer_class = SectionCRUDSerializer
    queryset = Section.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamTemplateCreateAPIView(BaseCreatorCreateAPIView):
    serializer_class = ExamTemplateCreateUpdateSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamTemplateDropdownListAPIView(ListAPIView):
    serializer_class = ExamTemplateMiniSerializer
    queryset = ExamTemplate.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]

    def get_queryset(self):
        return super().get_queryset().filter(status=ExamTemplateStatus.COMPLETED)


class ExamTemplateListAPIView(ListAPIView):
    serializer_class = ExamTemplateCreateUpdateSerializer
    queryset = ExamTemplate.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamTemplateRetrieveAPIView(RetrieveAPIView):
    serializer_class = ExamTemplateRetrieveSerializer
    queryset = ExamTemplate.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamTemplateUpdateAPIView(BaseCreatorUpdateAPIView):
    serializer_class = ExamTemplateCreateUpdateSerializer
    queryset = ExamTemplate.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamTemplateDeleteAPIView(DestroyAPIView):
    queryset = ExamTemplate.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class OptionCreateAPIView(CreateAPIView):
    serializer_class = OptionCUDSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class OptionUpdateAPIView(UpdateAPIView):
    serializer_class = OptionCUDSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]
    queryset = Question.objects.all()


class OptionsDeleteAPIView(DestroyAPIView):
    serializer_class = OptionCUDSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class QuestionDeleteAPIView(DestroyAPIView):
    queryset = Question.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamCreateAPIView(BaseCreatorCreateAPIView):
    serializer_class = ExamCreateSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamUpdateAPIView(BaseCreatorUpdateAPIView):
    serializer_class = ExamUpdateSerializer
    queryset = Exam.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamDeleteAPIView(DestroyAPIView):
    queryset = Exam.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamListAPIView(ListAPIView):
    serializer_class = ExamListAdminSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_class = ExamOnCourseFilter
    queryset = Exam.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamListOverviewAPIView(ExamListAPIView):
    serializer_class = ExamListOverviewAdminSerializer


class ExamOverviewCardAPIView(GenericAPIView):
    serializer_class = ExamOverviewCardSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]
    queryset = Exam.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class ExamDropdownListAPIView(ListAPIView):
    serializer_class = ExamMiniSerializer
    queryset = Exam.objects.all()
    permission_classes = [
        IsAdminOrSuperAdminOrDirector | IsAccountant | IsCashier | IsContentCreator
    ]


class ExamRetrieveAPIView(RetrieveAPIView):
    serializer_class = ExamRetrieveAdminSerializer
    queryset = Exam.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamImageUploadAPIView(CreateAPIView):
    serializer_class = ExamImageAdminSerializer
    # permission_classes = [IsAdminOrSuperAdminOrDirector]

    def perform_create(self, serializer):
        exam_id = self.kwargs.get("exam_id")
        exam = get_object_or_404(Exam, id=exam_id)
        return serializer.save(exam=exam)


class ExamDetailAPIView(RetrieveAPIView):
    serializer_class = ExamDetailSerializer
    queryset = Exam.objects.all()
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsContentCreator]


class ExamGeneratorAPIView(BaseReportGeneratorAPIView):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    queryset = Exam.objects.all()
    filterset_class = ExamOnCourseFilter
    model_name = "Exam"

    def get(self, request):
        return Response(
            {
                "model_fields": [
                    "exam",
                    "exam_type",
                    "exam_date",
                    "examinee",
                    "passes",
                    "failed",
                ]
            }
        )
