import calendar

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from accounts.models import UserRoles
from courses.models import Course
from dashboard.api_admin.serializers import (
    DashboardOverviewSerializer,
    DashboardRevenueCourseSerializer,
    DashboardRevenueGraphSerializer,
    DashboardRevenueSerializer,
)
from enrollments.models import Enrollment
from exams.models import Exam
from payments.models import Payment, PaymentStatus

User = get_user_model()


class DashboardOverviewAPIView(GenericAPIView):
    serializer_class = DashboardOverviewSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        date_time = timezone.localtime()
        revenue_list = (
            Payment.objects.filter(
                status=PaymentStatus.PAID, created_at__year=date_time.year
            )
            .aggregate(Sum("amount"))
            .get("amount__sum")
        )

        course_list = Course.objects.filter(created_at__year=date_time.year).count()

        exam_list = Exam.objects.filter(created_at__year=date_time.year).count()

        user_list = User.objects.filter(date_joined__year=date_time.year).count()

        course_enrollment_list = Enrollment.objects.filter(courses=None).count()

        students_list = (
            User.objects.filter(
                date_joined__year=date_time.year,
                role=UserRoles.STUDENT,
                enrolls__isnull=False,
            )
            .distinct()
            .count()
        )

        queryset = {
            "revenue": revenue_list,
            "courses": course_list,
            "exams": exam_list,
            "users": user_list,
            "course_enrollment": course_enrollment_list,
            "students": students_list,
        }
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class DashboardRevenueOverviewAPIView(GenericAPIView):
    serializer_class = DashboardRevenueSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        year = self.kwargs.get("year")
        date_time = timezone.localdate()

        revenue_overall = (
            Payment.objects.filter(status=PaymentStatus.PAID, created_at__year=year)
            .aggregate(Sum("amount"))
            .get("amount__sum")
        )

        revenue_month = (
            Payment.objects.filter(
                status=PaymentStatus.PAID,
                created_at__year=year,
                created_at__month=date_time.month,
            )
            .aggregate(Sum("amount"))
            .get("amount__sum")
        )

        queryset = {
            "revenue_overall": revenue_overall,
            "revenue_month": revenue_month,
        }
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class DashboardRevenueGraphAPIView(GenericAPIView):
    serializer_class = DashboardRevenueGraphSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        year = self.kwargs.get("year")

        payment = Payment.objects.filter(
            status=PaymentStatus.PAID, created_at__year=year
        ).order_by("-created_at")

        summary = (
            payment.annotate(g=ExtractMonth("created_at"))
            .values("g")
            .annotate(total=Sum("amount"))
            .order_by()
        )

        queryset = {calendar.month_name[i]: 0 for i in range(1, 13)}

        for summ in summary:
            queryset[calendar.month_name[summ["g"]]] = summ["total"]

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class DashboardRevenueCourseAPIView(GenericAPIView):
    serializer_class = DashboardRevenueCourseSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        year = self.kwargs.get("year")

        payment = Payment.objects.filter(
            status=PaymentStatus.PAID,
            created_at__year=year,
            enrollment__courses__isnull=False,
        ).order_by("-enrollment")

        summary = (
            payment.values("enrollment__courses__name")
            .annotate(total=Sum("amount"))
            .order_by()[:10]
        )

        serializer = self.get_serializer(summary, many=True)
        return Response(serializer.data)
