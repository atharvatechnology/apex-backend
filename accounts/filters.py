import django_filters
from django.contrib.auth import get_user_model

from accounts.models import Profile, Role
from common.utils import tuple_to_list_first_elements

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    """Filter for User."""

    role_wise = django_filters.CharFilter(method="roles_wise_filter")
    date_joined = django_filters.DateFromToRangeFilter(field_name="date_joined")
    is_enrolled = django_filters.BooleanFilter(method="is_enrolled_filter")

    class Meta:
        model = User
        fields = {
            "is_active": ["exact"],
            "roles": ["exact"],
        }

    def roles_wise_filter(self, queryset, name, value):
        if value == "Student":
            return queryset.filter(roles__in=[Role.STUDENT])
        elif value == "Faculty":
            return queryset.filter(
                roles__in=tuple_to_list_first_elements(Role.staff_choices)
            )
        return queryset

    def is_enrolled_filter(self, queryset, name, value):
        if value:
            return queryset.filter(enrolls__isnull=False)
        return queryset.filter(enrolls__isnull=True)


class StudentFilter(django_filters.FilterSet):
    """Filter for User."""

    class Meta:
        model = Profile
        fields = {"user__email": ["icontains"]}
