import django_filters

from .models import WebResouce


class WebResouceFilter(django_filters.FilterSet):
    """filter for web resource."""

    class Meta:
        model = WebResouce
        fields = {"title": ["icontains"]}
