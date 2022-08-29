from payments import PaymentStatus
from payments.gateways.base import BasicGateway


class EsewaGateway(BasicGateway):
    def capture(self, payment, amount):
        if payment.amount == amount:
            return PaymentStatus.PAID
            # TODO: Add payment verification
        else:
            return PaymentStatus.ERROR

    def verify():
        pass
