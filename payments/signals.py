from django.db.models.signals import post_save
from django.dispatch import receiver

from enrollments.api.utils import schedule_exam_in_five_minutes
from exams.models import ExamType
from payments import PaymentStatus


@receiver(post_save, sender="payments.OnlinePayment")
@receiver(post_save, sender="payments.BankPayment")
def on_online_payment(sender, instance, **kwargs):
    if instance.status == PaymentStatus.PAID:
        instance.enrollment.activate_enrollment()
        # schedule exam for enrollments into practice exams
        for exam_enrollment in instance.enrollment.exam_enrolls.filter(
            exam__exam_type=ExamType.PRACTICE
        ):
            # make new schedule for practice exams
            exam_session = schedule_exam_in_five_minutes(
                exam_enrollment.exam, instance.enrollment.student
            )
            exam_enrollment.selected_session = exam_session
            exam_enrollment.save()
