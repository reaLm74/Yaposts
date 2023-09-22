from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.conf import settings


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=200)
    text = forms.CharField(widget=forms.Textarea, label='Текст сообщения')
    email = forms.EmailField(label='Email')
    tel = forms.CharField(label='Номер телефона', required=False)
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox,
                               public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY,
                               label='ReCAPTCHA')
