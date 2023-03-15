from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView

from common.api.views import BaseCreatorCreateAPIView, BaseCreatorUpdateAPIView
from common.paginations import StandardResultsSetPagination
from common.permissions import IsAdminOrSuperAdminOrDirector
from discussion.models import Question

from .serializers import (
    QuestionAdminCreateSerializer,
    QuestionAdminListSerializer,
    QuestionAdminRetrieveSerializer,
    QuestionAdminUpdateSerializer,
)


# Create your views here.
class QuestionAdminCreateAPIView(BaseCreatorCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminCreateSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector]


class QuestionAdminListAPIView(ListAPIView):
    queryset = Question.objects.filter(question=None)
    serializer_class = QuestionAdminListSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector]
    pagination_class = StandardResultsSetPagination


class QuestionRepliesListAdminAPIView(ListAPIView):
    """View to retrieve replies for a specific question."""

    serializer_class = QuestionAdminListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        question_id = self.kwargs["pk"]
        question = Question.objects.get(id=question_id)
        return question.replies.all()


class QuestionAdminRetrieveAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminRetrieveSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector]
    pagination_class = StandardResultsSetPagination


class QuestionAdminUpdateAPIView(BaseCreatorUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminUpdateSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector]


class QuestionAdminDestroyAPIView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminRetrieveSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector]
