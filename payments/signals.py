from django.db.models.signals import post_save
from django.dispatch import receiver

from payments import PaymentStatus


@receiver(post_save, sender="payments.OnlinePayment")
@receiver(post_save, sender="payments.BankPayment")
def on_online_payment(sender, instance, **kwargs):
    if instance.status == PaymentStatus.PAID:
        instance.enrollment.activate_enrollment()
