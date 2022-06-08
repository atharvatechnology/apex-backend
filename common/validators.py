from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_positive(value):
    """Check if the value is positive number.

    Args:
        value (number): value to be validated

    Raises
        ValidationError: error with msg

    """
    if value < 0:
        raise ValidationError(
            _("%(value)s is not a positive number"),
            params={"value": value},
        )


def validate_date_time_gt_now(value):
    """Check if the value is greater than now.

    Args:
        value (datetime): value to be validated

    Raises
        ValidationError: error with msg

    """
    if value <= timezone.now():
        phrase1 = "should be greater"
        phrase2 = "than current date and time."
        raise ValidationError(
            _(f"{value.strftime('%Y-%m-%d %H:%M %p')} {phrase1} {phrase2} "),
            params={"value": value},
        )
