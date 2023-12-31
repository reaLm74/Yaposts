# Generated by Django 4.2.4 on 2023-09-04 01:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('user',), 'verbose_name': 'Телефон, адрес, дата рождения', 'verbose_name_plural': 'Телефоны, адреса, даты рождений'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=30, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tel',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
