from django.urls import path

from payments.api_admin.views import PaymentListAPIView

app_name = "admin-payments"

urlpatterns = [
    path("list/", PaymentListAPIView.as_view(), name="payment-list"),
]
