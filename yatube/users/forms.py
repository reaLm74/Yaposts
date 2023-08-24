from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    """Добавляем дополнительное поле в форму регистрации"""
    tel = forms.CharField(label='Введите номер телефона', initial='+7 (999) 888-66-55', help_text='Tel', error_messages={'required': 'Please enter your tel'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'tel')
