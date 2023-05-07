from django.urls import path

from exams.api.views import (
    ExamListAPIView,
    ExamPaperAPIView,
    ExamPaperPreviewAPIView,
    ExamRetrieveAPIView,
    ExamRetrievePoolAPIView,
    MyExamsList,
    trigger_exam_submit,
)

urlpatterns = [
    path("list/", ExamListAPIView.as_view(), name="exam-list"),
    path("my/", MyExamsList.as_view(), name="exam-my"),
    path("retrieve/<int:pk>/", ExamRetrieveAPIView.as_view(), name="exam-retrieve"),
    path(
        "retrieve/<int:pk>/pool/",
        ExamRetrievePoolAPIView.as_view(),
        name="exam-retrieve-pool",
    ),
    path(
        "paper/<int:pk>/<int:session_id>/",
        ExamPaperAPIView.as_view(),
        name="exam-paper",
    ),
    path(
        "paper/preview/<int:pk>/",
        ExamPaperPreviewAPIView.as_view(),
        name="exam-paper-preview",
    ),
    path(
        "trigger-submit/<int:pk>/",
        trigger_exam_submit,
        name="trigger-exam-submit",
    ),
]
