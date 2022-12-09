import django_filters

from accounts.models import Profile, Role, User


class UserFilter(django_filters.FilterSet):
    """Filter for User."""

    roles = django_filters.CharFilter(method="roles_wise_filter")

    class Meta:
        model = User
        fields = {"is_active": ["exact"]}

    def roles_wise_filter(self, queryset, name, value):
        if value == "Student":
            return queryset.filter(roles__in=[Role.STUDENT])
        elif value == "Faculty":
            return queryset.filter(roles__in=[1, 2, 3, 4, 5, 6, 7, 8])
        return queryset


class StudentFilter(django_filters.FilterSet):
    """Filter for User."""

    class Meta:
        model = Profile
        fields = {"user__email": ["icontains"]}
