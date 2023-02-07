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
from discussion.permissions import DiscussionPermission
# Create your views here.

class QuestionCreateAPIView(BaseCreatorCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    permission_classes=[DiscussionPermission]

class QuestionListAPIView(ListAPIView):
    serializer_class = QuestionListSerializer
    permission_classes=[DiscussionPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return Question.objects.filter(created_by=user)
        return Question.objects.all()
    
class QuestionRetrieveAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionRetrieveSerializer
    permission_classes=[DiscussionPermission]

class QuestionUpdateAPIView(BaseCreatorUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionUpdateSerializer
    permission_classes=[DiscussionPermission]

class QuestionDestroyAPIView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionRetrieveSerializer
    permission_classes=[DiscussionPermission]


