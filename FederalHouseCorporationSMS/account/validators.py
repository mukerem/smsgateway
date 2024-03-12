import os
from django.core.exceptions  import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.validators import RegexValidator

def email_validate(email_address):
    try:
        validate_email(email_address)
    except ValidationError as e:
        return 0
    else:
        return 1


phone_number_validator = RegexValidator(
        regex=r"^((251)|(\+251)|(00251)|(0)|)[7-9][0-9]{8}$",
        message="Enter a valid phone number.",
    )