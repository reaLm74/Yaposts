# Generated by Django 4.2.4 on 2023-09-06 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_comment_options_alter_group_options_and_more'),
        ('users', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favourite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.post'),
        ),
    ]