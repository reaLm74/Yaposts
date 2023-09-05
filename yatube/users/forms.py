from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory

from .models import Profile

User = get_user_model()


class CreationForm(UserCreationForm):
    """Добавляем дополнительное поле в форму регистрации"""
    recaptcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
        label='ReCAPTCHA'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'recaptcha'
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('tel', 'location', 'birth_date')
        widgets = {
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
        }


ExpansionCreationForm = inlineformset_factory(
    User, Profile, form=ProfileForm, fields=[
        'tel', 'location', 'birth_date'
    ], can_delete_extra=False
)
