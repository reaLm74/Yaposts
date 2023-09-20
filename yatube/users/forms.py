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

#
# class UserEditForm(UserChangeForm):
#     password = None
#
#     class Meta:
#         model = User
#         fields = (
#             'first_name',
#             'last_name',
#
#             'email',
#         )
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             # 'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#         }
#
#
# class ProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('tel', 'location', 'birth_date', 'user')
#         widgets = {
#             'tel': forms.TextInput(attrs={'class': 'form-control'}),
#             'location': forms.TextInput(attrs={'class': 'form-control'}),
#             'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
#         }
#
#
# ExpansionEditForm = inlineformset_factory(
#     User,
#     Profile,
#     form=ProfileEditForm,
#     fields=['tel', 'location', 'birth_date'],
#     can_delete=False
# )
#
#
# class EmployeeEditForm(forms.ModelForm):
#     #fields from User model that you want to edit
#     first_name = forms.CharField(required=False, label=('first_name'))
#     last_name = forms.CharField(required=False, label=('last_name'))
#     birth_date = forms.CharField(required=False, label=('birth_date'))
#
#     class Meta:
#         model = Profile
#         fields = ('first_name', 'last_name', 'tel', 'location', 'birth_date')
