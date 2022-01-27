from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class AlphabeticPasswordValidator(object):
    def validate(self, password, user=None):
        if password.isalpha():
            raise ValidationError(
                _("Password alphabetic"), code="password_entirely_alphabetic"
            )

    # Default help texts are replaced in the modal so we can just return empty string here.
    def get_help_text(self):
        return ""
