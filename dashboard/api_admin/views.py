import calendar

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Role
from attendance.models import StudentAttendance, TeacherAttendance
from common.permissions import IsSuperAdminorDirector
from courses.models import Course, CourseCategory
from dashboard.api_admin.filters import CourseCategoryFilter, ExamDateFilter
from dashboard.api_admin.serializers import (
    DashboardEnrollmentCountSerializer,
    DashboardOverviewSerializer,
    DashboardRevenueCourseSerializer,
    DashboardRevenueGraphSerializer,
    DashboardRevenueSerializer,
)
from enrollments.models import Enrollment, EnrollmentStatus
from exams.models import Exam
from payments.models import Payment, PaymentStatus

User = get_user_model()


class DashboardOverviewAPIView(GenericAPIView):
    serializer_class = DashboardOverviewSerializer
    permission_classes = [IsSuperAdminorDirector]

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

        course_enrollment_list = Enrollment.objects.filter(
            courses__isnull=False
        ).count()

        students_list = (
            User.objects.filter(
                date_joined__year=date_time.year,
                roles__id=Role.STUDENT,
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
    permission_classes = [IsSuperAdminorDirector]

    def get(self, request, *args, **kwargs):
        date_time = timezone.localdate()

        revenue_overall = (
            Payment.objects.filter(
                status=PaymentStatus.PAID, created_at__year=date_time.year
            )
            .aggregate(Sum("amount"))
            .get("amount__sum")
        )

        revenue_month = (
            Payment.objects.filter(
                status=PaymentStatus.PAID,
                created_at__year=date_time.year,
                created_at__month=date_time.month,
            )
            .aggregate(Sum("amount"))
            .get("amount__sum")
            or 0
        )
        date_time_prev = date_time - relativedelta(months=1)

        revenue_prev_month = (
            Payment.objects.filter(
                status=PaymentStatus.PAID,
                created_at__year=date_time_prev.year,
                created_at__month=date_time_prev.month,
            )
            .aggregate(Sum("amount"))
            .get("amount__sum")
            or 0
        )
        print(revenue_month, revenue_prev_month)
        trend = ((revenue_month - revenue_prev_month) / revenue_prev_month) * 100

        queryset = {
            "revenue_overall": revenue_overall,
            "revenue_month": revenue_month,
            "revenue_month_trend": trend,
        }
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class DashboardRevenueGraphAPIView(GenericAPIView):
    serializer_class = DashboardRevenueGraphSerializer
    permission_classes = [IsSuperAdminorDirector]

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
    permission_classes = [IsSuperAdminorDirector]

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


class DashboardEnrollmentOverallCourseAPIView(APIView):
    permission_classes = [IsSuperAdminorDirector]

    def get(self, request, *args, **kwargs):
        year = self.kwargs.get("year")

        enrollments = Enrollment.objects.filter(
            courses__isnull=False,
            created_at__year=year,
        )

        course_category = CourseCategory.objects.all()

        overall_section = {"overall": enrollments.count()}
        overall_section["active"] = enrollments.filter(
            status=EnrollmentStatus.ACTIVE
        ).count()

        for cat in course_category:
            overall_section[cat.name] = enrollments.filter(
                courses__category=cat
            ).count()

        return Response(overall_section)


class DashboardEnrollmentCourseCategoryAPIView(ListAPIView):
    permission_classes = [IsSuperAdminorDirector]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseCategoryFilter
    queryset = Course.objects.all()
    serializer_class = DashboardEnrollmentCountSerializer

    def get(self, request, *args, **kwargs):
        year = self.kwargs.get("year")
        enrollments = Enrollment.objects.filter(
            courses__isnull=False,
            created_at__year=year,
        )
        courses = self.filter_queryset(self.get_queryset())
        data = []
        for course in courses:
            course_enrollemt_count = {
                "name": course.name,
                "count": enrollments.filter(courses__in=[course]).count(),
            }
            data.append(course_enrollemt_count)
        sorted_data = sorted(data, key=lambda item: item["count"], reverse=True)
        serializer = self.get_serializer(sorted_data, many=True)
        return Response(serializer.data)


class DashboardEnrollmentExamCountAPIView(ListAPIView):
    permission_classes = [IsSuperAdminorDirector]
    serializer_class = DashboardEnrollmentCountSerializer
    queryset = Enrollment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExamDateFilter

    def get(self, request, *args, **kwargs):

        enrollments = self.filter_queryset(self.get_queryset())
        enrollments = enrollments.filter(
            exams__isnull=False,
        )
        exams = Exam.objects.all()

        data = []
        for exam in exams:
            exam_enrollemt_count = {
                "name": exam.name,
                "count": enrollments.filter(exams__in=[exam]).count(),
            }
            data.append(exam_enrollemt_count)
        sorted_data = sorted(data, key=lambda item: item["count"], reverse=True)
        serializer = self.get_serializer(sorted_data, many=True)
        return Response(serializer.data)


class DashboardAttendanceAPIView(APIView):
    permission_classes = [IsSuperAdminorDirector]

    def get(self, request, *args, **kwargs):
        student_attendance = StudentAttendance.objects.filter(
            date__date=timezone.now().date()
        ).count()
        teacher_attendance = TeacherAttendance.objects.filter(
            date__date=timezone.now().date()
        ).count()
        return Response(
            {
                "student_attendance": student_attendance,
                "teacher_attendance": teacher_attendance,
            }
        )
