from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class AgeValidator:
    def __call__(self, value):
        if value:
            if not all([
                    value > 5,
                    value < 130,
            ]):
                raise ValidationError(
                    _('Please enter a valid age')
                )
