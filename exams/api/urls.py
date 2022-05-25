from django.urls import path

from exams.api.views import (
    ExamCreateAPIView,
    ExamDeleteAPIView,
    ExamListAPIView,
    ExamPaperAPIView,
    ExamRetrieveAPIView,
    ExamTemplateCreateAPIView,
    ExamTemplateDeleteAPIView,
    ExamTemplateListAPIView,
    ExamTemplateRetrieveAPIView,
    ExamTemplateUpdateAPIView,
    ExamUpdateAPIView,
)

urlpatterns = [
    path("create/", ExamCreateAPIView.as_view(), name="exam-create"),
    path("list/", ExamListAPIView.as_view(), name="exam-list"),
    path("retrieve/<int:pk>/", ExamRetrieveAPIView.as_view(), name="exam-retrieve"),
    path("update/<int:pk>/", ExamUpdateAPIView.as_view(), name="exam-update"),
    path("delete/<int:pk>/", ExamDeleteAPIView.as_view(), name="exam-delete"),
    path("paper/<int:pk>/", ExamPaperAPIView.as_view(), name="exam-paper"),
]

urlpatterns += [
    path(
        "template/create/",
        ExamTemplateCreateAPIView.as_view(),
        name="exam-template-create",
    ),
    path(
        "template/list/", ExamTemplateListAPIView.as_view(), name="exam-template-list"
    ),
    path(
        "template/retrieve/<int:pk>/",
        ExamTemplateRetrieveAPIView.as_view(),
        name="exam-template-retrieve",
    ),
    path(
        "template/update/<int:pk>/",
        ExamTemplateUpdateAPIView.as_view(),
        name="exam-template-update",
    ),
    path(
        "template/delete/<int:pk>/",
        ExamTemplateDeleteAPIView.as_view(),
        name="exam-template-delete",
    ),
]
