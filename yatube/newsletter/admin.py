from django.contrib import admin

from .models import Newsletters


@admin.register(Newsletters)
class NewslettersAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')
