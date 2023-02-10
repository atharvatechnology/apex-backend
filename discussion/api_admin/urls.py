from django.urls import path
from .views import(
QuestionAdminListAPIView,
QuestionAdminCreateAPIView,
QuestionAdminRetrieveAPIView,
QuestionAdminUpdateAPIView,
QuestionAdminDestroyAPIView
)

app_name = "discussion.api_admin"

urlpatterns = [
    path('list/',QuestionAdminListAPIView.as_view(),name='admin-question-list'),
    path('create/',QuestionAdminCreateAPIView.as_view(),name='admin-question-create'),
    path('retrieve/<int:pk>/',QuestionAdminRetrieveAPIView.as_view(),name='admin-question-retrieve'),
    path('update/<int:pk>/',QuestionAdminUpdateAPIView.as_view(),name='admin-question-update'),
    path('delete/<int:pk>/',QuestionAdminDestroyAPIView.as_view(),name='admin-question-delete'),
]