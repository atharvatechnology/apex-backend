from functools import cached_property

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class ZeroSecondDateTimeField(models.DateTimeField):
    """Zero second DateTimeField."""

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.replace(second=0, microsecond=0)

    def to_python(self, value):
        value = super().to_python(value)
        return value.replace(second=0, microsecond=0)


class PercentageField(models.DecimalField):
    """PercentageField with range 0-1."""

    default_error_messages = {
        "invalid": _("“%(value)s” value must be a between 0 and 1."),
    }

    def __init__(self, *args, **kwargs):
        kwargs["help_text"] = _("Enter value between 0 and 1.")
        super().__init__(*args, **kwargs)

    @cached_property
    def validators(self):
        return super().validators + [
            MinValueValidator(0),
            MaxValueValidator(1),
        ]
