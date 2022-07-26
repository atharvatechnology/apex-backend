import django_filters

from accounts.models import User


class UserFilter(django_filters.FilterSet):
    """Filter for api_admin."""

    class Meta:
        model = User
        fields = {"is_active": ["exact"]}
