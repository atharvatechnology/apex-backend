from celery import shared_task

from enrollments.api.utils import dynamic_excel_generator


@shared_task
def excelcelery(filtered_data, data):
    dynamic_excel_generator(filtered_data, data)
