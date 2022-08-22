from django.urls import path

from ..api.views import (
    BankPaymentCreateAPIView,
    OnlinePaymentCreateAPIView,
    OnlinePaymentUpdateAPIView,
)

urlpatterns = [
    path(
        "onlinepay/create", OnlinePaymentCreateAPIView.as_view(), name="online-create"
    ),
    path(
        "onlinepay/update/<int:pk>/",
        OnlinePaymentUpdateAPIView.as_view(),
        name="online-update",
    ),
    path("bankpay/create", BankPaymentCreateAPIView.as_view(), name="bank-create"),
]
