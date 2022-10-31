import django_filters

from exams.models import Exam


class ExamFilter(django_filters.FilterSet):
    """filter for exam course."""

    class Meta:
        model = Exam
        fields = {"course": ["exact"], "name": ["icontains"]}


class ExamOnCourseFilter(django_filters.FilterSet):
    """filter for exam course."""

    class Meta:
        model = Exam
        fields = {"course_id": ["exact"]}
