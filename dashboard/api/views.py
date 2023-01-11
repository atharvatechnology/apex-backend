from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from exams.models import Exam
from notes.models import Content


class DashboardViewCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        course_count = Course.objects.filter(is_published=True).count()
        exam_count = Exam.objects.filter(is_published=True).count()
        content_count = Content.objects.all().count()

        data = {
            "course": course_count,
            "exam": exam_count,
            "content": content_count,
        }
        return Response(data)
