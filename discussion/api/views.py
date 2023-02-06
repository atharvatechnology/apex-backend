from rest_framework.generics import(
ListAPIView,
RetrieveAPIView,
DestroyAPIView,
)
from common.api.views import (
    BaseCreatorCreateAPIView,
    BaseCreatorUpdateAPIView
)
from discussion.models import Question

from . serializers import (
    QuestionListSerializer,
    QuestionRetrieveSerializer,
    QuestionUpdateSerializer,
    QuestionCreateSerializer
)

# Create your views here.

class QuestionCreateAPIView(BaseCreatorCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    
class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    
class QuestionRetrieveAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionRetrieveSerializer

class QuestionUpdateAPIView(BaseCreatorUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionUpdateSerializer
    
class QuestionDestroyAPIView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionRetrieveSerializer

