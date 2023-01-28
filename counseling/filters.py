import django_filters

from counseling.models import Counseling


class CounselingFilter(django_filters.FilterSet):
    """Filter for courses."""

    class Meta:
        model = Counseling
        fields = {"counsellor": ["exact"], "created_at": ["exact", "gte", "lte"]}
