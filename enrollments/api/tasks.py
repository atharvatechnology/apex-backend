from celery import shared_task
from enrollments.models import ExamThroughEnrollment
from common.utils import dynamic_excel_generator

@shared_task
def Excelcelery(model_name, model_fields):
    dynamic_excel_generator(model_name,model_fields)