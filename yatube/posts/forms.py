from django import forms
from django.core.exceptions import ValidationError

from .models import *

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image', 'is_published')
        help_texts = {
            "text": "Введите текст статьи",
            "group": "Выберите группу",
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if title == '':
            raise ValidationError('Статья с таким заголовком уже существует.')
        return title

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['group'].empty_label = "Группа не выбрана"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {
            "text": "Напишите комментарий"
        }
