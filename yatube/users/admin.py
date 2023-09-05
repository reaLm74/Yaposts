from django import forms
from django.contrib import admin

from .models import Profile


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'tel', 'location', 'birth_date',)
    search_fields = ('text',)
    empty_value_display = '-пусто-'
    list_per_page = 10
