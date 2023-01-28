from django.urls import include, path

from exams.api_admin.views import (
    ExamCreateAPIView,
    ExamDeleteAPIView,
    ExamDetailAPIView,
    ExamDropdownListAPIView,
    ExamImageUploadAPIView,
    ExamListAPIView,
    ExamListOverviewAPIView,
    ExamOverviewCardAPIView,
    ExamRetrieveAPIView,
    ExamTemplateCreateAPIView,
    ExamTemplateDeleteAPIView,
    ExamTemplateDropdownListAPIView,
    ExamTemplateListAPIView,
    ExamTemplateRetrieveAPIView,
    ExamTemplateUpdateAPIView,
    ExamUpdateAPIView,
    OptionCreateAPIView,
    OptionsDeleteAPIView,
    OptionUpdateAPIView,
    QuestionCreateAPIView,
    QuestionUpdateAPIView,
    SectionCreateAPIView,
    SectionDeleteAPIView,
    SectionUpdateAPIView,
)

exam_overview_urls = [
    path("", ExamListOverviewAPIView.as_view(), name="exam-overview-list"),
    path("card/", ExamOverviewCardAPIView.as_view(), name="exam-overview-card"),
]

urlpatterns = [
    path("create/", ExamCreateAPIView.as_view(), name="exam-create"),
    path("update/<int:pk>/", ExamUpdateAPIView.as_view(), name="exam-update"),
    path("delete/<int:pk>/", ExamDeleteAPIView.as_view(), name="exam-delete"),
    path("list/", ExamListAPIView.as_view(), name="exam-list"),
    path(
        "list/dropdown/", ExamDropdownListAPIView.as_view(), name="exam-list-dropdown"
    ),
    path("retrieve/<int:pk>/", ExamRetrieveAPIView.as_view(), name="exam-retrieve"),
    path(
        "upload/<int:exam_id>/",
        ExamImageUploadAPIView.as_view(),
        name="exam-image-upload",
    ),
    path("detail/<int:pk>/", ExamDetailAPIView.as_view(), name="exam-detail"),
    path("overview/", include(exam_overview_urls)),
]

option_urls = [
    path("create/", OptionCreateAPIView.as_view(), name="option-create"),
    path("update/<int:pk>/", OptionUpdateAPIView.as_view(), name="option-update"),
    path("delete/<int:pk>/", OptionsDeleteAPIView.as_view(), name="option-delete"),
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
        "list/dropdown/",
        ExamTemplateDropdownListAPIView.as_view(),
        name="template-list-dropdown",
    ),
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
