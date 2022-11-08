from django.urls import include, path

from ..api.views import (
    BankPaymentCreateAPIView,
    MonthlyRevenueBarGraph,
    OnlinePaymentCreateAPIView,
    OnlinePaymentUpdateAPIView,
    TopRevenueAmount,
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

graph_urls = [path("bar/", MonthlyRevenueBarGraph.as_view(), name="monthly-bar")]
urlpatterns = [
    path("onlinepay/", include(online_urls)),
    path("bankpay/", include(bank_urls)),
    path("payment-graph/", include(graph_urls)),
    path("top-revenue/", TopRevenueAmount.as_view(), name="top-revenue"),
]
