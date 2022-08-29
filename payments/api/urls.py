from django.urls import include, path

from ..api.views import (
    BankPaymentCreateAPIView,
    OnlinePaymentCreateAPIView,
    OnlinePaymentUpdateAPIView,
)

bank_urls = [path("create/", BankPaymentCreateAPIView.as_view(), name="bank-create")]

online_urls = [
    path("create/", OnlinePaymentCreateAPIView.as_view(), name="online-create"),
    path(
        "update/<int:pk>/",
        OnlinePaymentUpdateAPIView.as_view(),
        name="online-update",
    ),
]
urlpatterns = [
    path("onlinepay/", include(online_urls)),
    path("bankpay/", include(bank_urls)),
]
