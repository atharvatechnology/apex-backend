from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags

from apex.celery import app

# import cv2
# import qrcode


# def generate_qrcode(data, file_path):
#     """Generate qr code for data.

#     Parameters
#     ----------
#     data : str
#         data to be encoded in qr code.
#     file_path : str
#         path to file
#     """
#     img = qrcode.make(data)
#     img.save(file_path)


# def read_qrcode(file_path):
#     """read the image and return the data.

#         Parameters
#         ----------
#         file_path : str
#             path to file

#     #     Returns
#     #     -------
#     #     _data: str
#     #         detect the qr code from img and return the data.
#     #"""

#     img = cv2.imread(file_path)
#     detector = cv2.QRCodeDetector()
#     data, bbox, straight_qrcode = detector.detectAndDecode(img)
#     return data
"""file contains utility functions for the project."""


def get_human_readable_date_time(data):
    """Get human readable date time."""
    return data.strftime("%Y-%m-%d %H:%M %p")


def send_mail_common(template, context, to, subject):
    htmly = get_template(template)
    from_email = settings.EMAIL_HOST_USER
    html_content = htmly.render(context)
    text_content = strip_tags(html_content)
    # msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()
    async_send_mail.delay(subject, text_content, from_email, to, html_content)


@app.task
def async_send_mail(subject, text_content, from_email, to, html_content):
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def excelgenerator(models,obj):
    import xlsxwriter

    if models == "ExamThroughEnrollment":
        workbook = xlsxwriter.Workbook('enrollment.xlsx')
        worksheet = workbook.add_worksheet('task')
        worksheet.write(0, 0,'S.No')
        worksheet.write(0, 1,'Student Name')
        worksheet.write(0, 2,'Exam')
        worksheet.write(0, 3,'Selected Session')
        worksheet.write(0, 4,'Question')
        worksheet.write(0, 5,'Score')
        worksheet.write(0, 6,'Status')

        for index, entry in enumerate(obj):
            question = entry.exam.questions.all()
            worksheet.write(index+1, 0, str(index))
            worksheet.write(index+1, 1, str(entry.enrollment.student.first_name)+str(entry.enrollment.student.last_name))
            worksheet.write(index+1, 2, entry.exam.name)
            worksheet.write(index+1, 3, str(entry.selected_session.start_date))
            for i in question:
                worksheet.write(index+1, 4, len(question))
            worksheet.write(index+1, 5, entry.score)
            worksheet.write(index+1, 6, entry.status)
    
        workbook.close()

    elif models == "Exam":
        workbook = xlsxwriter.Workbook('exam.xlsx')
        worksheet = workbook.add_worksheet('task')
        worksheet.write(0, 0, 's.no')
        worksheet.write(0, 1, 'Name')
        worksheet.write(0, 2, 'Category')
        worksheet.write(0, 3, 'Status')
        worksheet.write(0, 4, 'Price')
        for index, entry in enumerate(obj):
            worksheet.write(index+1, 0, str(index))
            worksheet.write(index+1, 1, entry.name)
            worksheet.write(index+1, 2, entry.category.name)
            worksheet.write(index+1, 3, entry.status)
            worksheet.write(index+1, 4, entry.price)
        workbook.close()

    else:
        pass   
    workbook.close()
    
    
    