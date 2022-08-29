class PaymentStatus:
    UNPAID = "unpaid"  # Aswaiting payment
    INPROGRESS = "inprogress"  # verification in progress
    PAID = "paid"  # payment success
    ERROR = "error"  # verification error
    CHOICES = [
        (UNPAID, "unpaid"),
        (INPROGRESS, "inprogress"),
        (PAID, "paid"),
        (ERROR, "error"),
    ]
