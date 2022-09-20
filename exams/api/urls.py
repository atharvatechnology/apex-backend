from django.urls import path

from exams.api.views import (
    ExamListAPIView,
    ExamPaperAPIView,
    ExamPaperPreviewAPIView,
    ExamRetrieveAPIView,
    ExamRetrievePoolAPIView,
)

urlpatterns = [
    path("list/", ExamListAPIView.as_view(), name="exam-list"),
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
]
