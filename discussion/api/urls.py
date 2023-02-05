from django.urls import path
from .views import(
QuestionListAPIView,
QuestionCreateAPIView,
QuestionRetrieveAPIView,
QuestionUpdateAPIView,
QuestionDestroyAPIView
)

app_name = "discussion.api"

urlpatterns = [
    path('list/',QuestionListAPIView.as_view(),name='listquestion'),
    path('create/',QuestionCreateAPIView.as_view(),name='createquestion'),
    path('retrieve/<int:pk>/',QuestionRetrieveAPIView.as_view(),name='retrievequestion'),
    path('update/<int:pk>/',QuestionUpdateAPIView.as_view(),name='updatequestion'),
    path('delete/<int:pk>/',QuestionDestroyAPIView.as_view(),name='deletequestion'),
]