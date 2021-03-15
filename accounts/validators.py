from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email_unique(value):
    exists = User.objects.filter(email__iexact=value)

    if exists:
        raise ValidationError('Another account is already using this email address.'
                              'Please try another.')

def clean_client_phone(self):
    phone = self.cleaned_data.get('client_phone', None)
    try:
        if long(client_phone) and not client_phone.isalpha():
            min_length = 10
            max_length = 13
            ph_length = str(client_phone)
            if len(ph_length) < min_length or len(ph_length) > max_length:
                raise ValidationError('Phone number length not valid')

    except (ValueError, TypeError):
        raise ValidationError('Please enter a valid phone number')
    return client_phone
