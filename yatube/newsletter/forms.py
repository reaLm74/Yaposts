from django import forms

from .models import Newsletters


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletters
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Email address...'})
        }
