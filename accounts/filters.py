import django_filters

from accounts.models import Profile, Role, User
from common.utils import tuple_to_list_first_elements


class UserFilter(django_filters.FilterSet):
    """Filter for User."""

    role_wise = django_filters.CharFilter(method="roles_wise_filter")

    class Meta:
        model = User
        fields = {"is_active": ["exact"], "roles": ["exact"]}

    def roles_wise_filter(self, queryset, name, value):
        if value == "Student":
            return queryset.filter(roles__in=[Role.STUDENT])
        elif value == "Faculty":
            return queryset.filter(
                roles__in=tuple_to_list_first_elements(Role.staff_choices)
            )
        return queryset


class StudentFilter(django_filters.FilterSet):
    """Filter for User."""

    class Meta:
        model = Profile
        fields = {"user__email": ["icontains"]}
