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
    path('list/',QuestionListAPIView.as_view(),name='question-list'),
    path('create/',QuestionCreateAPIView.as_view(),name='question-create'),
    path('retrieve/<int:pk>/',QuestionRetrieveAPIView.as_view(),name='question-retrieve'),
    path('update/<int:pk>/',QuestionUpdateAPIView.as_view(),name='question-update'),
    path('delete/<int:pk>/',QuestionDestroyAPIView.as_view(),name='question-delete'),
]