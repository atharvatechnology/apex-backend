from datetime import datetime

import django_filters
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_filters.filters import _truncate

from courses.models import Course
from exams.models import Exam
from payments.models import Payment


def last_n_months(month):
    today = now()
    start_of_toady = datetime(today.year, today.month, 1)
    start_of_n_months_ago = start_of_toady - relativedelta(months=month)
    return _truncate(start_of_n_months_ago), _truncate(start_of_toady)


def last_n_year(year):
    today = now()
    start_of_this_year = datetime(today.year, 1, 1)
    start_of_last_year = start_of_this_year - relativedelta(years=year)
    return _truncate(start_of_last_year), _truncate(start_of_this_year)


class CustomDateRangeFilter(django_filters.DateRangeFilter):
    choices = [
        ("today", _("Today")),
        ("this month", _("This month")),
        ("last 3 months", _("Last 3 months")),
        ("last 6 months", _("Last 6 months")),
        ("last year", _("Last year")),
    ]

    filters = {
        "today": lambda qs, name: qs.filter(
            **{
                f"{name}__year": now().year,
                f"{name}__month": now().month,
                f"{name}__day": now().day,
            }
        ),
        "this month": lambda qs, name: qs.filter(
            **{f"{name}__year": now().year, f"{name}__month": now().month}
        ),
        "last 3 months": lambda qs, name: qs.filter(
            **{f"{name}__gte": last_n_months(3)[0], f"{name}__lte": last_n_months(3)[1]}
        ),
        "last 6 months": lambda qs, name: qs.filter(
            **{f"{name}__gte": last_n_months(6)[0], f"{name}__lte": last_n_months(6)[1]}
        ),
        "last year": lambda qs, name: qs.filter(
            **{f"{name}__gte": last_n_year(1)[0], f"{name}__lte": last_n_year(1)[1]}
        ),
    }


payment_choices_type = (
    ("Course", "Course"),
    ("Exam", "Exam"),
    ("All", "All"),
)


class PaymentFilter(django_filters.FilterSet):
    created_at = CustomDateRangeFilter()
    custom_created_at = django_filters.DateFromToRangeFilter(field_name="created_at")
    payment_category = django_filters.TypedChoiceFilter(
        choices=payment_choices_type, method="payment_category_filter"
    )
    exam = django_filters.ModelChoiceFilter(
        field_name="enrollment__exams",
        queryset=Exam.objects.all(),
    )
    course = django_filters.ModelChoiceFilter(
        field_name="enrollment__courses",
        queryset=Course.objects.all(),
    )

    class Meta:
        model = Payment
        fields = (
            "created_at",
            "custom_created_at",
            "payment_category",
            "exam",
            "course",
        )

    def payment_category_filter(self, queryset, name, value):
        if value == "Course":
            return queryset.filter(enrollment__courses__isnull=False)
        elif value == "Exam":
            return queryset.filter(enrollment__exams__isnull=False)
        else:
            return queryset
