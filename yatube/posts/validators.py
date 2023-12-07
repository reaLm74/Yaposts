from django.core.exceptions import ValidationError


def validate_not_empty(value):
    # Проверка "а заполнено ли поле?"
    if len(value) == 1:
        print('Please enter')
        raise ValidationError(
            'Кто поле будет заполнять?',
            params={'value': value}, code='invalid'
        )
