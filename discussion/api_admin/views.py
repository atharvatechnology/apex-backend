from django.shortcuts import get_object_or_404
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
        """Get the queryset containing all replies to a particular question.

        Returns
            QuerySet: The queryset containing all replies to the specified question.

        Raises
            Http404: If the question with the specified ID does not exist.

        """
        # Get the question ID from the URL kwargs
        question_id = self.kwargs.get("pk")
        if question_id is None:
            # If no ID is found, return an empty queryset
            return Question.objects.none()
        # Get the question object with the given ID
        # If the question doesn't exist, raise an HTTP 404 error
        question = get_object_or_404(Question, id=question_id)
        # Return a queryset of all replies to the question
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
