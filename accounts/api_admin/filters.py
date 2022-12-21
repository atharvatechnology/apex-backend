import django_filters
from django.contrib.auth import get_user_model

from accounts.models import Role
from common.utils import tuple_to_list_first_elements

User = get_user_model()


class UserAdminFilter(django_filters.FilterSet):
    """Filter for User."""

    role_wise = django_filters.CharFilter(method="roles_wise_filter")
    date_joined = django_filters.DateFromToRangeFilter(field_name="date_joined")

    class Meta:
        model = User
        fields = {
            "is_active": ["exact"],
            "roles": ["exact"],
        }

    def roles_wise_filter(self, queryset, name, value):
        if value == "Faculty":
            return queryset.filter(
                roles__in=tuple_to_list_first_elements(Role.staff_choices)
            )
        elif value == "Staff":
            return queryset.filter(
                roles__in=tuple_to_list_first_elements(Role.trackable_staff_choices)
            )
        return queryset


class StudentAdminFilter(django_filters.FilterSet):
    """Filter for Student User."""

    date_joined = django_filters.DateFromToRangeFilter(field_name="date_joined")
    is_enrolled = django_filters.BooleanFilter(method="is_enrolled_filter")

    class Meta:
        model = User
        fields = {
            "is_active": ["exact"],
        }

    def is_enrolled_filter(self, queryset, name, value):
        if value:
            return queryset.filter(enrolls__isnull=False).distinct()
        return queryset.filter(enrolls__isnull=True).distinct()


class FacultyAdminFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "roles": ["exact"],
        }
