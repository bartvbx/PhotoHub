from django.core.exceptions import ValidationError


def file_size_validator(file):
    limit = 5 * 1024 * 1024
    if file.size > limit:
        raise ValidationError('Yout photo size is too large. It should not exceed 5 MBs.')
