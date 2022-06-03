from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from exams.models import Exam, ExamStatus, ExamTemplate

from .serializers import (
    ExamCreateSerializer,
    ExamListSerializer,
    ExamPaperSerializer,
    ExamRetrieveSerializer,
    ExamTemplateSerializer,
    ExamUpdateSerializer,
)


class ExamCreateAPIView(BaseCreatorCreateAPIView):
    serializer_class = ExamCreateSerializer
    # permission_classes = [AllowAny]


class ExamListAPIView(ListAPIView):
    serializer_class = ExamListSerializer
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()


class ExamRetrieveAPIView(RetrieveAPIView):
    serializer_class = ExamRetrieveSerializer
    permission_classes = [AllowAny]
    queryset = Exam.objects.all()


class ExamUpdateAPIView(BaseCreatorUpdateAPIView):
    serializer_class = ExamUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()


class ExamPaperAPIView(RetrieveAPIView):
    serializer_class = ExamPaperSerializer
    permission_classes = [IsAuthenticated]  # TODO: IsEnrolled
    queryset = Exam.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == ExamStatus.IN_PROGRESS:
            return super().retrieve(request, *args, **kwargs)
        return Response({"detail": "Exam is not in progress"}, status=400)


class ExamDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()


class ExamTemplateCreateAPIView(BaseCreatorCreateAPIView):
    serializer_class = ExamTemplateSerializer
    # permission_classes = []


class ExamTemplateListAPIView(ListAPIView):
    serializer_class = ExamTemplateSerializer
    # TODO: permit admin only
    # permission_classes = []
    queryset = ExamTemplate.objects.all()


class ExamTemplateRetrieveAPIView(RetrieveAPIView):
    serializer_class = ExamTemplateSerializer
    queryset = ExamTemplate.objects.all()


class ExamTemplateUpdateAPIView(BaseCreatorUpdateAPIView):
    serializer_class = ExamTemplateSerializer
    # TODO: permit admin only
    # permission_classes = []
    queryset = ExamTemplate.objects.all()


class ExamTemplateDeleteAPIView(DestroyAPIView):
    # TODO: permit admin only
    permission_classes = [IsAuthenticated]
    queryset = ExamTemplate.objects.all()
