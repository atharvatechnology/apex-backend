from rest_framework.generics import(
ListAPIView,
RetrieveAPIView,
DestroyAPIView,
)
from common.api.views import (
    BaseCreatorCreateAPIView,
    BaseCreatorUpdateAPIView
)
from common.permissions import IsAdminOrSuperAdminOrDirector
from discussion.models import Question

from . serializers import (
    QuestionAdminListSerializer,
    QuestionAdminRetrieveSerializer,
    QuestionAdminUpdateSerializer,
    QuestionAdminCreateSerializer
)
# Create your views here.

class QuestionAdminCreateAPIView(BaseCreatorCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminCreateSerializer
    permission_classes=[IsAdminOrSuperAdminOrDirector]

class QuestionAdminListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminListSerializer
    permission_classes=[IsAdminOrSuperAdminOrDirector]
    
class QuestionAdminRetrieveAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminRetrieveSerializer
    permission_classes=[IsAdminOrSuperAdminOrDirector]

class QuestionAdminUpdateAPIView(BaseCreatorUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminUpdateSerializer
    permission_classes=[IsAdminOrSuperAdminOrDirector]

class QuestionAdminDestroyAPIView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminRetrieveSerializer
    permission_classes=[IsAdminOrSuperAdminOrDirector]


