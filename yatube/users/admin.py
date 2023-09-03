from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.admin import UserAdmin
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

