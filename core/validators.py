from rest_framework.exceptions import ValidationError


def validate_phone_number(value):
    if not str(value).isdigit() or len(str(value)) != 10:
        raise ValidationError('Phone number must be a 10-digit number.')


def validate_rating(value):
    if not isinstance(value, int) or value < 1 or value > 5:
        raise ValidationError('Rating must be between 1 and 5.')


def validate_pan_number(value):
    if not str(value).isdigit() or len(str(value)) != 10:
        raise ValidationError('Pan number must be a 10-digit number.')


def validate_zip_code(value):
    if not str(value).isdigit() or len(str(value)) != 5:
        raise ValidationError('Zip code must be a 5-digit number.')