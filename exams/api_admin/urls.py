from django.urls import include, path

from exams.api_admin.views import (
    ExamCreateAPIView,
    ExamDeleteAPIView,
    ExamListAPIView,
    ExamRetrieveAPIView,
    ExamTemplateCreateAPIView,
    ExamTemplateDeleteAPIView,
    ExamTemplateListAPIView,
    ExamTemplateRetrieveAPIView,
    ExamTemplateUpdateAPIView,
    ExamUpdateAPIView,
    QuestionCreateAPIView,
    QuestionUpdateAPIView,
    SectionCreateAPIView,
    SectionDeleteAPIView,
    SectionUpdateAPIView,
)

urlpatterns = [
    path("create/", ExamCreateAPIView.as_view(), name="exam-create"),
    path("update/<int:pk>/", ExamUpdateAPIView.as_view(), name="exam-update"),
    path("delete/<int:pk>/", ExamDeleteAPIView.as_view(), name="exam-delete"),
    path("list/", ExamListAPIView.as_view(), name="exam-list"),
    path("retrieve/<int:pk>/", ExamRetrieveAPIView.as_view(), name="exam-retrieve"),
]

question_urls = [
    path("create/", QuestionCreateAPIView.as_view(), name="question-create"),
    path("update/<int:pk>/", QuestionUpdateAPIView.as_view(), name="question-update"),
]

section_urls = [
    path("create/", SectionCreateAPIView.as_view(), name="section-create"),
    path("update/<int:pk>/", SectionUpdateAPIView.as_view(), name="section-update"),
    path("delete/<int:pk>/", SectionDeleteAPIView.as_view(), name="section-delete"),
]

template_urls = [
    path("section/", include(section_urls)),
    path("create/", ExamTemplateCreateAPIView.as_view(), name="template-create"),
    path("list/", ExamTemplateListAPIView.as_view(), name="template-list"),
    path(
        "retrieve/<int:pk>/",
        ExamTemplateRetrieveAPIView.as_view(),
        name="template-retrieve",
    ),
    path(
        "update/<int:pk>/", ExamTemplateUpdateAPIView.as_view(), name="template-update"
    ),
    path(
        "delete/<int:pk>/", ExamTemplateDeleteAPIView.as_view(), name="template-delete"
    ),
]

urlpatterns += [
    path("questions/", include(question_urls)),
    path("template/", include(template_urls)),
]
