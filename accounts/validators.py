from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    """
    Making a username behave as phone number
    """

    regex = r"^\+?1?\d{9,15}$"
    message = _(
        "Enter a valid phone number. This value may contain only numbers, "
        "and must be between 9 and 15 characters long."
    )
    flags = 0
