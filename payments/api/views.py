import calendar

from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from courses.models import CourseCategory
from payments import PaymentStatus
from payments.api.serializers import (
    BankPaymentCreateSerializer,
    OnlinePaymentCreateSerializer,
    OnlinePaymentUpdateSerializer,
    PaymentCreateSerializer,
)
from payments.filters import PaymentDateFilter
from payments.models import BankPayment, OnlinePayment, Payment

# class PaymentCreateAPIView(CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = PaymentCreateSerializer
#     queryset = Payment.objects.all()


class OnlinePaymentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlinePaymentCreateSerializer
    queryset = OnlinePayment.objects.all()


class BankPaymentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankPaymentCreateSerializer
    queryset = BankPayment.objects.all()


class OnlinePaymentUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlinePaymentUpdateSerializer
    queryset = OnlinePayment.objects.all()


class MonthlyRevenueBarGraph(ListAPIView):
    """Total revenue got from exam and course(frame18) bar graph."""

    permission_classes = [IsAdminUser]
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = PaymentDateFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().filter(status=PaymentStatus.PAID)
        )
        months = [payment.created_at.date().month for payment in queryset]
        months = sorted(set(months))
        months.sort()
        data = []
        for month in months:
            monthly_payments = queryset.filter(created_at__month=month)
            net_amount = sum(
                monthly_payment.amount for monthly_payment in monthly_payments
            )
            data.append(
                {"month": calendar.month_name[month], "paid_amount": net_amount}
            )
        return Response(data, status=status.HTTP_200_OK)


class TopRevenueAmount(MonthlyRevenueBarGraph):
    """Top Revenue by category."""

    def list(self, request, *args, **kwargs):
        data = []
        course_category = CourseCategory.objects.all()
        for category in course_category:
            net_amt = 0
            for course in category.courses.all():
                for enroll in course.enrolls.all():
                    enrol = enroll.payments_payment_related.filter(
                        status=PaymentStatus.PAID
                    ).aggregate(total=Sum("amount"))
                    if enrol["total"] is not None:
                        net_amt += enrol["total"]
            data.append({category.name: net_amt})
        return Response(data, status=status.HTTP_200_OK)
