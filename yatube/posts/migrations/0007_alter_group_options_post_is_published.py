# Generated by Django 4.2.4 on 2023-08-09 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_comment_id_alter_follow_id_alter_group_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('title',), 'verbose_name': 'Сообщество', 'verbose_name_plural': 'Сообщества'},
        ),
        migrations.AddField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Публикация'),
        ),
    ]
