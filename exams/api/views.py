from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from courses.api.paginations import StandardResultsSetPagination
from exams.api.permissions import IsExamEnrolledActive
from exams.models import Exam, ExamStatus

from .serializers import (  # ExamUpdateSerializer,
    ExamListSerializer,
    ExamPaperSerializer,
    ExamRetrievePoolSerializer,
    ExamRetrieveSerializer,
)

# class ExamCreateAPIView(BaseCreatorCreateAPIView):
#     serializer_class = ExamCreateSerializer
#     # permission_classes = [AllowAny]


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
        if instance.status == ExamStatus.IN_PROGRESS:
            return super().retrieve(request, *args, **kwargs)
        return Response({"detail": "Exam is not in progress"}, status=400)


class ExamPaperPreviewAPIView(RetrieveAPIView):
    serializer_class = ExamPaperSerializer
    permission_classes = [IsAdminUser]
    queryset = Exam.objects.all()
