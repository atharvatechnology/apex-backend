from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_positive(value):
    """Check if the value is positive number.

    Args:
        value (number): value to be validated

    Raises:
        ValidationError: error with msg
    """
    if value < 0:
        raise ValidationError(
            _("%(value)s is not a positive number"),
            params={"value": value},
        )
