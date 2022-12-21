import django_filters

from accounts.models import Profile


class StudentFilter(django_filters.FilterSet):
    """Filter for User."""

    class Meta:
        model = Profile
        fields = {"user__email": ["icontains"]}
