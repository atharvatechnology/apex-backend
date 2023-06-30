import calendar
from datetime import datetime

from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Role, User
from common.permissions import IsAdminOrSuperAdminOrDirector
from courses.models import CourseCategory
from enrollments.models import ExamSession, ExamThroughEnrollment, SessionStatus
from exams.models import Exam
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

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = PaymentDateFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().filter(status=PaymentStatus.PAID)
        )
        data = []
        for month in range(1, 13):
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


class DashboardOverview(ListAPIView):
    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentDateFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().filter(status=PaymentStatus.PAID)
        )
        new_list = []
        net_amt_this_year = sum(this_month.amount for this_month in queryset)
        new_list.append({"revenue": net_amt_this_year})
        total_active_course_enrollment = 0
        course_category = CourseCategory.objects.all()
        for category in course_category:
            for course in category.courses.all():
                active_enrollment = course.enrolls.all().count()

                total_active_course_enrollment += active_enrollment
        new_list.append(
            {
                "course_enroll": total_active_course_enrollment,
            }
        )
        exams = Exam.objects.all()
        exam_enrollment_count = 0
        for exam in exams:
            enrollment = ExamThroughEnrollment.objects.filter(exam__id=exam.id).count()
            exam_enrollment_count += enrollment
        overall_enrollment = exam_enrollment_count + total_active_course_enrollment
        new_list.extend(
            (
                {"exam_enrolled": exam_enrollment_count},
                {"total_enrollment": overall_enrollment},
            )
        )

        exam_session = ExamSession.objects.filter(status=SessionStatus.ACTIVE)
        total_exam_enrollment = 0
        for session in exam_session:
            enrollments = ExamThroughEnrollment.objects.filter(exam__id=session.exam.id)
            if enrollments:
                total_exam_enrollment += 1
        new_list.append({"active_exam": total_exam_enrollment})
        student_count = User.objects.filter(roles__id=Role.STUDENT).count()
        teacher_count = User.objects.filter(roles__id=Role.TEACHER).count()
        new_list.extend(
            ({"teacher_count": teacher_count}, {"student_count": student_count})
        )
        return Response(new_list, status=status.HTTP_200_OK)


class RevenueOverView(ListAPIView):

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().filter(status=PaymentStatus.PAID)
        )
        data = []
        payment_this_year = queryset.filter(created_at__year=datetime.now().year)
        payment_previous_year = queryset.filter(
            created_at__year=datetime.now().year - 1
        )
        net_amt_this_year = sum(this_month.amount for this_month in payment_this_year)
        net_amt_previous_year = sum(
            this_month.amount for this_month in payment_previous_year
        )
        yearly_trend_amt = net_amt_this_year + net_amt_previous_year

        trend_percentage_year = net_amt_this_year / yearly_trend_amt * 100

        payment_this_month = queryset.filter(created_at__month=datetime.now().month)
        payment_previous_month = queryset.filter(
            created_at__month=datetime.now().month - 1
        )
        net_amt_this_month = sum(this_month.amount for this_month in payment_this_month)
        net_amt_previous_month = sum(
            this_month.amount for this_month in payment_previous_month
        )
        monthly_trend_amt = net_amt_this_month + net_amt_previous_month
        trend_percentage_month = net_amt_this_month / monthly_trend_amt * 100
        data.append(
            {
                "current_month_amt": net_amt_this_month,
                "trend_percentage": trend_percentage_month,
                "overall_amt": net_amt_this_year,
                "yearly_trend": trend_percentage_year,
            }
        )
        return Response(data, status=status.HTTP_200_OK)
