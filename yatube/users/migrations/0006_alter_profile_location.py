# Generated by Django 4.2.6 on 2023-11-01 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_favourite_profile_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Адрес'),
        ),
    ]
