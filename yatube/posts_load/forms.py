from django import forms


class PostLoadForm(forms.Form):
    file = forms.FileField(label='')
