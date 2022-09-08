from celery import shared_task
from enrollments.models import ExamThroughEnrollment
from common.utils import excelgenerator

@shared_task
def Excelcelery(model_name,pk_list):
    qs = ExamThroughEnrollment.objects.filter(id__in=pk_list)
    excelgenerator(model_name, qs)
 