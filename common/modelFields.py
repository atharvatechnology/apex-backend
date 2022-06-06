from django.db import models


class ZeroSecondDateTimeField(models.DateTimeField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.replace(second=0, microsecond=0)

    def to_python(self, value):
        value = super().to_python(value)
        return value.replace(second=0, microsecond=0)
