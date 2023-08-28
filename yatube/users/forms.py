from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
User = get_user_model()


class CreationForm(UserCreationForm):
    """Добавляем дополнительное поле в форму регистрации"""
    tel = forms.CharField(label='Введите номер телефона', initial='+7 (999) 888-66-55', error_messages={'required': 'Please enter your tel'})
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'tel', 'password1', 'password2', 'recaptcha')
