import django_filters

from accounts.models import Profile, User


class UserFilter(django_filters.FilterSet):
    """Filter for User."""

    class Meta:
        model = User
        fields = {"is_active": ["exact"]}


class StudentFilter(django_filters.FilterSet):
    """Filter for User."""

    class Meta:
        model = Profile
        fields = {"user__email": ["icontains"]}
