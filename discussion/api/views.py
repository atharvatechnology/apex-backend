from rest_framework.generics import(
CreateAPIView,
ListAPIView,
RetrieveAPIView,
UpdateAPIView,
DestroyAPIView,
)
from discussion.models import Question
from . serializers import QuestionSerializer
# Create your views here.

class QuestionCreateAPIView(CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
class QuestionRetrieveAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionUpdateAPIView(UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
class QuestionDestroyAPIView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

